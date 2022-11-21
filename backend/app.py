from flask import Flask, render_template, request, send_file
from helpers.database import db, Site, User, Machine, Activity
from classes.qr_generator import QRBlueprint
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from classes.auth import Auth
from datetime import *
import subprocess
import time

# The Framework class sets up our Backend Web Framework Flask. Like almost every
# other Python web framework, flask is meant to be functional, so we have to make
# added classes like Framework to force it to work in an OO manor. This holds the
# Flask App framework that is used in App and AppWrapper
class Framework:
    def __init__(self):
        self.login_manager = LoginManager()
        self.login_manager.login_view = 'login'
        self.app = Flask(__name__)

# The App class acts as a Model class. It's function is to implement the functionality
# of our application. It uses Framework to access our Web Framework and then provides functions
# that can be called by AppWrapper, the controller, to process data requests
class App:

    def __init__(self, Frame, appopt=None, manager=None):

        self.manager = manager
        self.application = appopt

        self.login_session = {}

        self.app = Frame.app
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        self.app.config['SECRET_KEY'] = 'login-manager-admin'

        self.db = db
        self.db.app = self.app
        self.db.init_app(self.app)

        with self.app.app_context():
            self.db.create_all()

        Frame.login_manager.init_app(self.app)

    def register(self, username, passwrd, site_post):

        response = {'exists':0, 'success': 0} 
        AuthAgent = Auth()

        password = AuthAgent.hash_key(passwrd)

        if User.query.filter_by(username=username).first():
            response['exists'] = 1
            response['success'] = 1 
            return response # sends back a failure as a response, user exists

        new_user = User(username=username, password=password, site=site_post)
        new_site = Site(name=site_post)


        self.db.session.add(new_user)
        self.db.session.add(new_site)

        self.db.session.commit()

        response['success'] = 0

        return response

    def login(self, username, passwrd):

        response = {"user": 0, "pass": 0, "loggedin": 0}
        AuthAgent = Auth()
        user = User.query.filter_by(username=username).first()

        if user:
            if AuthAgent.verify_key(user.password, passwrd):
                
                response['loggedin'] = 1
                login_user(user)
                self.login_session['username'] = user.username
                self.login_session['site'] = user.site
                return response
            else:
                response['pass'] = 1
                return response  
        else:
            response['user'] = 1
            return response

    def new_machine(self, time, site, machine_type):

        if request.method == 'POST':

            switch = {'wash': '1', 'dry': '2', 'other': '3'}

            machine_id = str(switch[machine_type]) + str(datetime.now().timestamp()).replace('.','')
            
            new_machine = Machine(id=machine_id, time=time, site=site, broken=0)

            QRCreator = QRBlueprint(is_new=1, code_int=machine_id)
            route = QRCreator.create_code()

            self.db.session.add(new_machine)
            self.db.session.commit()

            return route

        else:
            return 'new_machine is a POST only endpoint'

    def run_machine(self, machine_id, number):
        
        if Activity.query.filter_by(id=machine_id).first():

            return {'already_run': 1}

        machine = Machine.query.filter_by(id=machine_id).first()
        self.db.session.add(Activity(id=machine.id, time=time.time(), site=machine.site))
        self.db.session.commit()

        # commented out so i dont get a fat bill. uncomment before demo

        # subprocess.Popen(['python3', 'classes/SMS.py', number, str(machine.time)], \
        #     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return {'machine_time': str(Machine.query.get(machine_id).time)}

    def logout(self):
        logout_user()
        del self.login_session['site']
        del self.login_session['username']
        return {'loggedout': 1}

    def dashboard(self, arg_site):

        requested_site = arg_site

        if not Site.query.filter_by(name=requested_site).first():
            return {'site':'null'}

        machines = Machine.query.filter_by(site=requested_site)

        form = {'site': requested_site}
        for i in machines:

            if i.broken:
                form[str(i.id)] = -1
                continue


            j = Activity.query.filter_by(id=i.id).first()

            if j:
                if int(time.time() - j.time) >= int(j.time) or int(time.time() - j.time) < 0:
                    act = Activity.query.get(j.id)
                    self.db.session.delete(act)
                    self.db.session.commit()
                    form[str(j.id)] = 0
                else:    
                    temp_machine = Machine.query.filter_by(id=j.id).first()
                    form[str(j.id)] = str(temp_machine.time + int(j.time - time.time()))
                    if int(form[str(j.id)]) < 0:
                        act = Activity.query.get(j.id)
                        self.db.session.delete(act)
                        self.db.session.commit()
                        form[str(j.id)] = 0

            else:
                form[str(i.id)] = 0
        return form

    def getsite(self):
        return {'site': User.query.filter_by(username=self.login_session['username']).first().site}

    def check_login(self):

        response = {'loggedin':0}

        try:
            if self.login_session['username']:
                response['loggedin'] = 1
            return response

        except:
            return response

    def report_machine(self, machineid):

        machine = Machine.query.filter_by(id=machineid).first()
        new_machine = Machine(id=machineid, time=machine.time, site=machine.site, broken=1)
        delete = Machine.query.get(machineid)
        db.session.delete(delete)
        db.session.commit()
        db.session.add(new_machine)
        db.session.commit()

        return {'success':1}

    def fix_machine(self, machineid):

        machine = Machine.query.filter_by(id=machineid).first()
        new_machine = Machine(id=machineid, time=machine.time, site=machine.site, broken=0)
        delete = Machine.query.get(machineid)
        db.session.delete(delete)
        db.session.commit()
        db.session.add(new_machine)
        db.session.commit()

        return {'success':1}

    def homepage(self):

        # we can through some data return here so that we can display
        # messages on our 
        info_out = dict()
        info_out['title'] = 'Laundry Manager'
        info_out['ver']= 'beta_v1.0'

        return info_out

    def change_username(self, username):

        try:
            old_user = User.query.filter_by(username=self.login_session['username']).first()
            login_session['username'] = username
            new_user = User(username=username, password=old_user.password, site=old_user.site)
            db.session.delete(old_user)
            db.session.commit()
            db.session.add(new_user)
            db.session.commit()
            return {'success':1}

        except:
            return {'success':0}

    def change_password(self, new_password):
        AuthAgent = Auth()
        new_password = AuthAgent.hash_key(new_password)
        old_user = User.query.filter_by(username=self.login_session['username']).first()
        new_user = User(username=self.login_session['username'], password=new_password, site=old_user.site)
        db.session.delete(old_user)
        db.session.commit()
        db.session.add(new_user)
        db.session.commit()

        return {'success':1}


# Class AppWrapper acts as a controller class as it implements our routing system. It has
# two major components: routes, which is the controller implementation, implementing all flask
# framework endpoints and routing them to the proper App function that implements the requested
# functionality. NOTE: @app.route's are not nested functions! They are overrided to be used as 
# endpoints! Think of them as a variable that just redirects a web request! Without endpoints,
# we can't build an API. routes() has one more function, which is start. All this does is 
class AppWrapper:

    def __init__(self, start=0):

        self.flask_framework = Framework()
        self.app = self.flask_framework.app
        self.login_manager = self.flask_framework.login_manager
        self.app_router = App(self.flask_framework, '0.0.0.0', '5000')

    def routes(self, start):

        @self.app.route('/') # Functional
        def homepage():
            return self.app_router.homepage()

        @self.app.route('/loggedin') # Functional
        def check_login():
            return self.app_router.check_login()

        @self.app.route('/getsite') # Functional
        def getsite():
            return self.app_router.getsite()

        @self.app.route('/dashboard', methods=['POST']) # Functional -> bug, can be negative
        def dashboard():
            if request.method == "POST":
                return self.app_router.dashboard(request.args['site'])

        @self.app.route("/logout") # Functional
        def logout():
            try:
                return self.app_router.logout()
            except:
                return 'not logged in'

        @self.app.route("/run-machine", methods=['POST']) # Functional
        def run_machine():
            if request.method == "POST":
                return self.app_router.run_machine(request.args['machine'], request.args['number'])


        @self.app.route('/new-machine', methods=['POST']) # Functional
        def new_machine():

            if request.method == "POST":
                try:
                    return self.app_router.new_machine(request.args['time'], request.args['site'], request.args['type'])
                except:
                    return 'not logged in'

        @self.app.route('/login', methods=['POST']) # Functional
        def login():
            if request.method == "POST":
                username = request.args.get('username')
                password = request.args.get('password')
                return self.app_router.login(username, password)

        @self.app.route("/register", methods=['POST']) # Functional
        def register():

            if request.method == "POST":
                AuthAgent = Auth()
                username = request.args.get('username')
                password = request.args.get('password')
                site_post = request.args.get('site')
                return self.app_router.register(username, password, site_post)

        @self.login_manager.user_loader
        def load_user(user_id):
            print("USER ID", user_id)
            return User.query.get(int(user_id))

        @self.app.route('/report', methods=['POST'])
        def report():
            return self.app_router.report_machine(request.args['machine'])

        @self.app.route('/fixed', methods=['POST'])
        def fixed():
            return self.app_router.fix_machine(request.args['machine'])

        @self.app.route('/changeusername', methods=['POST'])
        def changeuser():
            return self.app_router.change_username(request.args['newname'])

        @self.app.route('/changepassword', methods=['POST'])
        def changepass():
            return self.app_router.change_password(request.args['newpass'])

        if start:
            self.app.run()
    

    def start(self):
        self.routes(True)


if __name__ == "__main__":
    application = AppWrapper(start=True)
    application.start()