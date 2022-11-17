import qrcode
import webbrowser
from classes.qr import QR
from flask import Blueprint, request
from datetime import *
import os

qr_code = Blueprint('qr_code', __name__)

@qr_code.route('/create-code', methods = ['GET', 'POST'])
def create_code(is_new=1, code_int=0):

	QRCode = QR(code_int)

	base = (request.base_url).split('new-machine')[0]

	print(code_int)
	QRCode.create_qr(base + 'run-machine?machine=')

	routing_code = QRCode.save_qr()

	if routing_code == -1:
	 	return "ERROR, Please Refresh the Page and Try again"

	return (routing_code + '.svg')

	#grab from database if not new





