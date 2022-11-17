from flask import Flask, render_template, request, send_file
from helpers.database import db, Site, User, Machine, Activity
from classes.qr_generator import QRBlueprint
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from classes.auth import Auth
from datetime import *
import time

class Framework:
    def __init__(self):

        self.login_manager = LoginManager()
        self.login_manager.login_view = 'login'
        self.app = Flask(__name__)


class App:

    def __init__(self, Frame, host, port, appopt=None, manager=None):

        self.manager = manager
        self.application = appopt

        login_manager = Frame.login_manager

        self.app = Frame.app
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        self.app.config['SECRET_KEY'] = 'login-manager-admin'

        self.db = db
        self.db.app = self.app
        self.db.init_app(self.app)

        with self.app.app_context():
            self.db.create_all()

        login_manager.init_app(self.app)

        self.host = host
        self.port = port

    def register(self, passwrd):

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

    def login(self, username, password):

        
        response = {"user": 0, "pass": 0, "loggedin": 0}
        AuthAgent = Auth()
        user = User.query.filter_by(username=username).first()
        if user:
            if AuthAgent.verify_key(user.password, password):
                response['loggedin'] = 1
                login_user(user, remember=True)
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
            
            new_machine = Machine(id=machine_id, time=time, site=site)

            QRCreator = QRBlueprint(is_new=1, code_int=machine_id)
            route = QRCreator.create_code()

            self.db.session.add(new_machine)
            self.db.session.commit()

            return send_file(route, mimetype='image/png')

        else:
            return 'new_machine is a POST only endpoint'

    def run_machine(self, machine_id):
        
        if Activity.query.filter_by(id=machine_id).first():
            return {'already_run': 1}

        machine = Machine.query.filter_by(id=machine_id).first()
        self.db.session.add(Activity(id=machine.id, time=time.time(), site=machine.site))
        self.db.session.commit()
        return {'machine_time': str(Machine.query.get(machine_id).time)}

    def logout(self):
        logout_user()
        return {'loggedout': 1}


    def dashboard(self, arg_site):

        requested_site = arg_site

        if not Site.query.filter_by(name=requested_site).first():
            return {'site':'null'}

        machines = Machine.query.filter_by(site=requested_site)

        form = {'site': requested_site}
        for i in machines:

            j = Activity.query.filter_by(id=i.id).first()

            if j:
                if int(time.time() - j.time) >= int(j.time):
                    Activity.query.filter_by(id=j.id).delete()
                    self.db.session.commit()
                else:    
                    temp_machine = Machine.query.filter_by(id=j.id).first()
                    form[str(j.id)] = str(temp_machine.time + int(j.time - time.time()))
            else:
                form[str(i.id)] = 0
        return form

    def getsite(self):
        return {'site': current_user.site}

    def check_login(self):

        response = {'loggedin':0}

        try:
            a = current_user.username
            response['loggedin'] = 1
            return reponse

        except:
            return response

    def homepage(self):

        # we can through some data return here so that we can display
        # messages on our 
        info_out = dict()
        info_out['title'] = 'Laundry Manager'
        info_out['ver']= 'beta_v1.0'

        return info_out

    def start(self):
        self.app.run(host=self.host, port=self.port)


class AppWrapper:

    def __init__(self, start=0):
        self.server = self.routes(start)

    def routes(self, start):

        flask_framework = Framework()
        app = flask_framework.app
        login_manager = flask_framework.login_manager

        self.app_router = App(flask_framework, '0.0.0.0', '5000')

        @app.route('/')
        def homepage():
            return self.app_router.homepage()

        @app.route('/loggedin')
        def check_login():
            return self.app_router.check_login()

        @app.route('/getsite')
        @login_required
        def getsite():
            return self.app_router.getsite()

        @app.route('/dashboard', methods=['POST'])
        def dashboard():
            if request.method == "POST":
                return self.app_router.dashboard(request.args['site'])

        @app.route("/logout")
        @login_required
        def logout():
            return self.app_router.logout()

        @app.route("/run-machine", methods=['POST'])
        def run_machine():
            if request.method == "POST":
                return self.app_router.run_machine(request.args['machine'])

        @app.route('/new-machine', methods=['POST'])
        @login_required
        def new_machine():

            if request.method == "POST":
                return self.app_router.new_machine(request.args['time'], request.args['site'], request.args['type'])

        @app.route('/login', methods=['POST'])
        def login():
            if request.method == "POST":
                username = request.args.get('username')
                password = request.args.get('password')
                return self.app_router.login(username, password)

        @app.route("/register", methods=['POST'])
        def register():

            if request.method == "POST":

                username = request.args.get('username')
                password = AuthAgent.hash_key(request.args.get('password'))
                site_post = request.args.get('site')
                return self.app_router.register(username, password, site_post)

        @login_manager.user_loader
        def get_user(userid):
            return User.query.get(int(userid))

        if start:
            app.run()
    


if __name__ == "__main__":
    application = AppWrapper(start=True)