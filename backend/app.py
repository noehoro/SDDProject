from flask import Flask, render_template, request
from helpers.database import db, Site, User, Machine, Activity
from qr_generator import qr_code
from auth import Auth

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.app = app
db.init_app(app)
db.create_all()
app.register_blueprint(qr_code)

@app.route("/register", methods=['POST'])
def register():

    print("GOT HERE")
    if request.method == "POST":
        response = {'exists':0, 'success': 0} 
        AuthAgent = Auth()

        print(request.args)
        username = request.args.get('username')
        
        password = AuthAgent.hash_key(request.args.get('password'))
        site = request.args.get('site')


        if User.query.filter_by(username=username).first():
            response['exists'] = 1
            response['success'] = 1 # Response code 1 is failure
            return response

        new_user = User(username=username, password=password, site_user=site)

        db.session.add(newUser)
        db.session.commit()

        response['success'] = 0

        return response

@app.route("/")
def homepage():
    return "running"

if __name__ == "__main__":
    app.run(debug=True)