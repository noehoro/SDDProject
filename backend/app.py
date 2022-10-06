from flask import Flask, render_template
from helpers.database import db
from qr_generator import qr_code

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(qr_code)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.app = app
db.init_app(app)
db.create_all()


@app.route("/")
def homepage():
    return render_template("homepage.html")

if __name__ == "__main__":
    app.run()