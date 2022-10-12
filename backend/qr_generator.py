import qrcode
import webbrowser
from qr import QR
from flask import Blueprint, request, send_file

qr_code = Blueprint('qr_code', __name__)

@qr_code.route('/create-code', methods = ['GET', 'POST'])
def create_code():

	if request.method == 'POST':
		
		code_int = int(request.args['cde'])
		
		QRCode = QR(code_int)
		QRCode.create_qr(request.base_url)

		base = (request.base_url).split('create-code')[0]

		QRCode.create_qr(base + 'machine/')

		routing_code = QRCode.save_qr()

		if routing_code == -1:
		 	return "ERROR, Please Refresh the Page and Try again"

		return send_file(routing_code + '.png', mimetype='image/png')

	elif request.method == 'GET':
		return "qr"

	else: 
		return "ERROR: "




