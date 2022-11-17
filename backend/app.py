from flask import Flask, render_template, request, send_file
from helpers.database import db, Site, User, Machine, Activity
from qr_generator import qr_code, create_code
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import *
import time
from classes.auth import Auth

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'login-manager-admin'

db.app = app
db.init_app(app)
with app.app_context():
    db.create_all()
app.register_blueprint(qr_code)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def get_user(userid):
    return User.query.get(int(userid))

@app.route("/register", methods=['POST'])
def register():

    if request.method == "POST":
        response = {'exists':0, 'success': 0} 
        AuthAgent = Auth()

        username = request.args.get('username')
        
        password = AuthAgent.hash_key(request.args.get('password'))
        site_post = request.args.get('site')


        if User.query.filter_by(username=username).first():
            response['exists'] = 1
            response['success'] = 1 
            return response # sends back a failure as a response, user exists

        new_user = User(username=username, password=password, site=site_post)
        new_site = Site(name=site_post)


        db.session.add(new_user)
        db.session.add(new_site)

        db.session.commit()

        response['success'] = 0

        return response

@app.route('/login', methods=['POST'])
def login():

    if request.method == 'POST':
        response = {"user": 0, "pass": 0, "loggedin": 0}
        AuthAgent = Auth()
        username = request.args.get('username')
        password = request.args.get('password')

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

@app.route('/new-machine', methods=['POST'])
@login_required
def new_machine():

    if request.method == 'POST':

        time = request.args['time']
        site = request.args['site']
        machine_type = request.args['type']

        switch = {'wash': '1', 'dry': '2', 'other': '3'}


        machine_id = str(switch[machine_type]) + str(datetime.now().timestamp()).replace('.','')
        
        new_machine = Machine(id=machine_id, time=time, site=site)
        route = create_code(is_new=1, code_int=machine_id)

        db.session.add(new_machine)
        db.session.commit()

        return send_file(route, mimetype='image/png')
    else:
        return 'new_machine is a POST only endpoint'



@app.route("/run-machine", methods=['POST'])
def run_machine():

    machine_id = request.args['machine']
    
    if Activity.query.filter_by(id=machine_id).first():
        return {'already_run': 1}

    machine = Machine.query.filter_by(id=machine_id).first()
    db.session.add(Activity(id=machine.id, time=time.time(), site=machine.site))
    db.session.commit()
    return {'machine_time': str(Machine.query.get(machine_id).time)}


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return {'loggedout': 1}


@app.route('/dashboard', methods=['POST'])
def dashboard():

    requested_site = request.args['site']

    if not Site.query.filter_by(name=requested_site).first():
        return {'site':'null'}

    machines = Activity.query.filter_by(site=requested_site)

    form = {'site': requested_site}
    for i in machines:

        if int(time.time() - i.time) >= int(i.time):
            Activity.query.filter_by(id=i.id).delete()
            db.session.commit()
        else:    
            temp_machine = Machine.query.filter_by(id=i.id).first()
            form[str(i.id)] = str(temp_machine.time + int(i.time - time.time()))

    return form

@app.route('/getsite')
def getsite():
    return {'site': current_user.site}


@app.route('/loggedin')
def check_login():

    response = {'loggedin':0}

    try:
        a = current_user.username
        response['loggedin'] = 1
        return reponse

    except:
        return response


@app.route("/")
def homepage():

    # we can through some data return here so that we can display
    # messages on our 
    info_out = dict()
    info_out['title'] = 'Laundry Manager'
    info_out['ver']= 'beta_v1.0'

    return info_out

if __name__ == "__main__":
    app.run()