import qrcode
import webbrowser
import qr
from flask import Blueprint, request, send_file

qr_code = Blueprint('qr_code', __name__)

@qr_code.route('/create-code', methods = ['POST'])
def create_code():
	if request.method == 'POST':
		code_int = int(request.form['cde'])
		QRCode = QR(code_int)

		routing_code = QRCode.save_qr()
		if routing_code == -1:
			return "ERROR, Please Refresh the Page and Try again"

		return send_file(routing_code, mimetype='image/png')



