from flask import Flask, render_template, request, send_file
from helpers.database import db, Site, User, Machine, Activity
from qr_generator import qr_code, create_code
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import *
from classes.auth import Auth
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'login-manager-admin'
CORS(app, supports_credentials=True, origins="*")


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
        response = {'exists': 0, 'success': 0}
        AuthAgent = Auth()

        username = request.get_json()['username']

        password = AuthAgent.hash_key(request.get_json()['password'])
        site_post = request.get_json()['site']

        if User.query.filter_by(username=username).first():
            response['exists'] = 1
            response['success'] = 1
            return response  # sends back a failure as a response, user exists

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
        username = request.get_json()['username']
        password = request.get_json()['password']

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
def new_machine():

    time = request.get_json()['time']
    site = request.get_json()['site']

    machine_id = int(str(datetime.now().timestamp()).replace('.', ''))

    new_machine = Machine(id=machine_id, time=time, site=site)
    route = create_code(is_new=1, code_int=machine_id)

    db.session.add(new_machine)
    db.session.commit()

    return send_file(route, mimetype='image/png')


@app.route("/run-machine", methods=['POST'])
def run_machine():

    machine_id = request.get_json()['machine']
    site = request.get_json()['site']
    time = int(str(datetime.now().timestamp()).replace('.', ''))
    new_activity = Activity(time=time,  machine_id=machine_id, site=site)

    db.session.add(new_activity)
    db.session.commit()
    return str(Machine.query.get(machine_id).time)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return {'loggedout': 1}


@app.route('/dashboard')
@login_required
def dashboard():

    machines = Machine.query.filter_by(site=current_user.site)

    form = {}
    for i in machines:
        form[i.id] = i.time

    return form


@app.route('/getsite')
def getsite():

    return {'site': current_user.site}


@app.route("/")
def homepage():

    # we can through some data return here so that we can display
    # messages on our
    info_out = dict()
    info_out['title'] = 'Laundry Manager'
    info_out['ver'] = 'beta_v1.0'

    return info_out


if __name__ == "__main__":
    app.run()
