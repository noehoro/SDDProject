from flask import Flask, render_template, request, send_file
from helpers.database import db, Site, User, Machine, Activity
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from classes.qr_generator import QRBlueprint
from classes.auth import Auth
from datetime import *
import subprocess
import time

'''
The Framework class sets up our Backend Web Framework Flask. Like almost every
other Python web framework, flask is meant to be functional, so we have to make
added classes like Framework to force it to work in an OO manor. This holds the
Flask App framework that is used in App and AppWrapper
'''
class Framework:
    def __init__(self):
        self.login_manager = LoginManager()
        self.login_manager.login_view = 'login'
        self.app = Flask(__name__)

'''
The App class acts as a Model class. It's function is to implement the functionality
of our application. It uses Framework to access our Web Framework and then provides functions
that can be called by AppWrapper, the controller, to process data requests
'''
class App:

    def __init__(self, Frame):

        # Create a login session to hold user data while they are using the site
        self.login_session = {}

        # Setup application from Frame (this is just config stuff to allow sqlalchemy and login to work)
        self.app = Frame.app
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        self.app.config['SECRET_KEY'] = 'login-manager-admin'

        # Tie database to application
        self.db = db
        self.db.app = self.app
        self.db.init_app(self.app)

        # Create all database instance classes
        with self.app.app_context():
            self.db.create_all()

        # Initialize login manager
        Frame.login_manager.init_app(self.app)

    # Function Register will Register a user account to our database
    def register(self, username, passwrd, site_post):

        # Create response form and Authorization agent to hash passwords
        response = {'exists':0, 'success': 0} 
        AuthAgent = Auth()

        # Hash password
        password = AuthAgent.hash_key(passwrd)

        # Check that username doesn't already exist 
        if User.query.filter_by(username=username).first():
            response['exists'] = 1
            response['success'] = 1 
            return response # sends back a failure as a response, user exists

        # Create new user and new site in database
        new_user = User(username=username, password=password, site=site_post)
        new_site = Site(name=site_post)

        # Commit to database
        self.db.session.add(new_user)
        self.db.session.add(new_site)

        self.db.session.commit()

        response['success'] = 0

        # Send response to caller
        return response

    # Login will try to login a user based off of username and password given
    def login(self, username, passwrd):

        # Create response form and Authorization client
        response = {"user": 0, "pass": 0, "loggedin": 0}
        AuthAgent = Auth()

        # try to find user through SQL query
        user = User.query.filter_by(username=username).first()

        # if user was found:
        if user:

            # try to verify user's password
            if AuthAgent.verify_key(user.password, passwrd):
                
                #Login user, add them to the login_session, and return response to client (success code)
                response['loggedin'] = 1
                login_user(user)
                print(user.username)
                print(user.site)
                self.login_session['username'] = user.username
                self.login_session['site'] = user.site
                return response

            # if not verified, specify the password was wrong and send response to client
            else:
                response['pass'] = 1
                return response  

        # If the user was not found, the username was wrong. Tell client
        else:
            response['user'] = 1
            return response

    # New machine creates a new Laundry machine for the user to have and use on their dash, 
    def new_machine(self, time, site, machine_type):

        if request.method == 'POST':
            print(time)
            print(site)
            print(machine_type)
            # Switch case for washer drier or other argument
            switch = {'wash': '1', 'dry': '2', 'other': '3'}

            # generate machine id (timestamp so they are all unique)
            machine_id = str(switch[machine_type]) + str(datetime.now().timestamp()).replace('.','')
            
            # Create machine database entry
            new_machine = Machine(id=machine_id, time=time, site=site, broken=0)

            # Get a QR code
            QRCreator = QRBlueprint(is_new=1, code_int=machine_id)
            route = QRCreator.create_code()

            # Commit the new machine to the db
            self.db.session.add(new_machine)
            self.db.session.commit()

            # Return the client the QR code
            return route

            
        else:
            return 'new_machine is a POST only endpoint'

    # Run_machine, well, runs a machine. When a machine is ran, it counts down during a subprocess
    def run_machine(self, machine_id, number):
        
        # Find if machine is already active
        if Activity.query.filter_by(id=machine_id).first():
            return {'already_run': 1}

        # find machine in query, commit to the database
        machine = Machine.query.filter_by(id=machine_id).first()
        self.db.session.add(Activity(id=machine.id, time=time.time(), site=machine.site))
        self.db.session.commit()

        # commented out so i dont get a fat bill. uncomment before demo

        # open a child process to handle SMS notifications 
        num = number.strip()
        numbertopass = "+" + number
        stdout_response = subprocess.Popen(['python3', 'classes/SMS.py', numbertopass, str(machine.time)], \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        print(stdout_response)
        # Return how much time this machine will take
        return {'machine_time': str(Machine.query.get(machine_id).time)}

    # Log the user out
    def logout(self):

        # Remove user from the session
        logout_user()
        del self.login_session['site']
        del self.login_session['username']

        # Return success to client
        return {'loggedout': 1}

    # Dashboard is the main page on the site, returns all machines active or inactive
    def dashboard(self, arg_site):

        requested_site = arg_site

        # Find if the site exsits, if not, finish here with a null return to client
        if not Site.query.filter_by(name=requested_site).first():
            return {'site':'null'}

        # Get all the machines in this site
        machines = Machine.query.filter_by(site=requested_site)

        # Setup response form, loop through each machine in the site found
        form = {'site': requested_site}
        for i in machines:

            # If the machine is marked broken, mark it and continue
            if i.broken:
                form[str(i.id)] = -1
                continue

            # Find if the machine is currently active
            j = Activity.query.filter_by(id=i.id).first()

            # if it is:
            if j:

                # calculate if it is finished, if it is, remove it from the database activity
                if int(time.time() - j.time) >= int(j.time) or int(time.time() - j.time) < 0:
                    act = Activity.query.get(j.id)
                    self.db.session.delete(act)
                    self.db.session.commit()
                    form[str(j.id)] = 0 
                else: # if it is not, send the user back remaining time. Handle special case where user requests at same time the machine is about
                      # to finish
                    temp_machine = Machine.query.filter_by(id=j.id).first()
                    form[str(j.id)] = str(temp_machine.time + int(j.time - time.time()))
                    if int(form[str(j.id)]) < 0:
                        act = Activity.query.get(j.id)
                        self.db.session.delete(act)
                        self.db.session.commit()
                        form[str(j.id)] = 0

            # if not found, it's not active. Specify that.
            else:
                form[str(i.id)] = 0

        # Return created form
        return form

    # GetSite does just that, returns the client the active user's site name
    def getsite(self):
        return {'site': User.query.filter_by(username=self.login_session['username']).first().site}

    # Check login just tells the client if the user is logged in our not. All it does is check if the user
    # is in the client login_session or not.
    def check_login(self):

        response = {'loggedin':0}

        try:
            if self.login_session['username']:
                response['loggedin'] = 1
            return response

        except:
            return response

    # Report machine will mark a machine as broken in the database
    def report_machine(self, machineid):

        # Find the machine requested, and create a copy of it but with the borken flag
        machine = Machine.query.filter_by(id=machineid).first()
        new_machine = Machine(id=machineid, time=machine.time, site=machine.site, broken=1)

        # delete the old machine
        delete = Machine.query.get(machineid)
        db.session.delete(delete)
        db.session.commit()

        # Commit the new copy
        db.session.add(new_machine)
        db.session.commit()

        # Return success to client
        return {'success':1}

    # Fix machine is the antithesis of report_machine, will mark a broken machine as fixed
    def fix_machine(self, machineid):

        # Get the broken machine from the database, create a copy without broken flag
        machine = Machine.query.filter_by(id=machineid).first() 
        new_machine = Machine(id=machineid, time=machine.time, site=machine.site, broken=0)

        # Delete broken machine from database
        delete = Machine.query.get(machineid)
        db.session.delete(delete)
        db.session.commit()

        # Commit the new copy
        db.session.add(new_machine)
        db.session.commit()

        # Return success to the client
        return {'success':1}

    # Homepage should not be accessed by the user, but can if they really want to. All it does is specify
    # the name and version. This is used to see if the application was running properly on a server or not.
    def homepage(self):

        # Return some data about the application (name and version)
        info_out = dict()
        info_out['title'] = 'Laundry Manager'
        info_out['ver']= 'beta_v1.0'

        # Send to client
        return info_out

    # Change username handles managers who want to change the username tied to their account 
    def change_username(self, username):

        # Similar structure to broken and fixed, but the try catch wrapper handles the unique username
        # protocol
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

    # Change password handles managers who need to change the password tied to their account
    def change_password(self, new_password):

        # Same as change_user, just hash value before committing as it is a password
        try:
            AuthAgent = Auth()
            new_password = AuthAgent.hash_key(new_password)
            old_user = User.query.filter_by(username=self.login_session['username']).first()
            new_user = User(username=self.login_session['username'], password=new_password, site=old_user.site)
            db.session.delete(old_user)
            db.session.commit()
            db.session.add(new_user)
            db.session.commit()
            return {'success':1}

        except:
            return {'success': 0}

'''
Class AppWrapper acts as a controller class as it implements our routing system. It has
two major components: routes, which is the controller implementation, implementing all flask
framework endpoints and routing them to the proper App function that implements the requested
functionality. NOTE: @app.route's are not nested functions! They are overrided to be used as 
endpoints! Think of them as a variable that just redirects a web request! Without endpoints,
we can't build an API. routes() has one more function, which is start. All this does is map out
the API endpoints to the App class.
'''
class AppWrapper:

    # Setup framework for App (constructor)
    def __init__(self, start=0):

        self.flask_framework = Framework()
        self.app = self.flask_framework.app
        self.login_manager = self.flask_framework.login_manager
        self.app_router = App(self.flask_framework)

    # Routes is the main function of the Wrapper. It is called when the application is ran
    # and adds all route codes to the application. NOTE: THESE ARE NOT FUNCTIONS! These are
    # are methods that have been overriden to act as URL endpoints!
    def routes(self, start):

        # Default route
        @self.app.route('/') # Functional
        def homepage():
            return self.app_router.homepage()

        #Login Route
        @self.app.route('/loggedin') # Functional
        def check_login():
            return self.app_router.check_login()

        # Get Site Route
        @self.app.route('/getsite') # Functional
        def getsite():
            return self.app_router.getsite()

        # Dashboard (main) route
        @self.app.route('/dashboard', methods=['POST']) # Functional -> bug, can be negative -> fixed
        def dashboard():
            if request.method == "POST":
                return self.app_router.dashboard(request.args['site'])

        # Logout route
        @self.app.route("/logout") # Functional
        def logout():
            try:
                return self.app_router.logout()
            except:
                return 'not logged in'

        # Run Machine Route
        @self.app.route("/run-machine", methods=['POST']) # Functional
        def run_machine():
            if request.method == "POST":
                return self.app_router.run_machine(request.args['machine'], request.args['number'])

        # New machine route
        @self.app.route('/new-machine', methods=['POST']) # Functional
        def new_machine():

            if request.method == "POST":
                try:
                    return self.app_router.new_machine(request.args['time'], request.args['site'], request.args['type'])
                except:
                    return 'not logged in'

        # Login Route
        @self.app.route('/login', methods=['POST']) # Functional
        def login():
            if request.method == "POST":
                username = request.args.get('username')
                password = request.args.get('password')
                return self.app_router.login(username, password)

        # Register Route
        @self.app.route("/register", methods=['POST']) # Functional
        def register():

            if request.method == "POST":
                AuthAgent = Auth()
                username = request.args.get('username')
                password = request.args.get('password')
                site_post = request.args.get('site_post')
                print(site_post)
                return self.app_router.register(username, password, site_post)

        # Load User (Route for login manager, inaccessable to user)
        @self.login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # Report Route
        @self.app.route('/report', methods=['POST'])
        def report():
            return self.app_router.report_machine(request.args['machine'])

        # Fixed Route
        @self.app.route('/fixed', methods=['POST'])
        def fixed():
            return self.app_router.fix_machine(request.args['machine'])

        # Change Username Route
        @self.app.route('/changeusername', methods=['POST'])
        def changeuser():
            return self.app_router.change_username(request.args['newname'])

        # Change Password Route
        @self.app.route('/changepassword', methods=['POST'])
        def changepass():
            return self.app_router.change_password(request.args['newpass'])

        # Apllication Startup Protocol. App.run() starts a server instance with
        # the open mappings, when start=True, the app will run
        if start:
            self.app.run()
    
    # Start is a function that will actually boot up the API application, so that it 
    # can be run throught a RESTful API
    def start(self):
        self.routes(True)


# Driver Code, this is what's run if you run this python file. Just starts the application on 
# a development server
if __name__ == "__main__":
    application = AppWrapper(start=True)
    application.start()