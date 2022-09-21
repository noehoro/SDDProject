from flask import Flask, render_template
from SQL.database import db, models*

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.app = app
db.init_app(app)
db.create_all()

@app.route("/")
def homepage():
    return render_template("homepage.html")