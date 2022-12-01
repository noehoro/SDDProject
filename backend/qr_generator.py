from classes.qr import QR
from flask import Blueprint, request
from datetime import *

qr_code = Blueprint('qr_code', __name__)


@qr_code.route('/create-code', methods=['GET', 'POST'])
def create_code(is_new=0, code_int=0):

    QRCode = QR(code_int)

    if is_new:
        base = "http://localhost:5173/new-machine/"

        QRCode.create_qr(base + f"{code_int}")

        routing_code = QRCode.save_qr()

        if routing_code == -1:
            return "ERROR, Please Refresh the Page and Try again"

        return (routing_code + '.png')

    # grab from database if not new

    else:
        return "ERROR: "
