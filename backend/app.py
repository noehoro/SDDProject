from flask import Flask
from qr_generator import qr_code
app = Flask(__name__)
app.register_blueprint(qr_code)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
