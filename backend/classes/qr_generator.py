import qrcode
import webbrowser
from classes.qr import QR
from flask import request
from datetime import *
import os

class QRBlueprint(object):

	def __init__(self, is_new=1, code_int=0):

		self.QRCode = QR(code_int)
		self.base = None
		self.routing_code = None

	def create_code(self):

		self.base = (request.base_url).split('new-machine')[0]

		self.QRCode.create_qr(self.base + 'run-machine?machine=')

		self.routing_code = self.QRCode.save_qr()

		if self.routing_code == -1:
		 	return "ERROR, Please Refresh the Page and Try again"

		return (self.routing_code + '.svg')