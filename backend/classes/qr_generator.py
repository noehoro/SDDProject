import qrcode
import webbrowser
from classes.qr import QR
from flask import request
from datetime import *
import os

'''
Class QRBlueprint acts as a Wrapper class for QR. QRCode creates QR codes using the QR class,
and then produces routing codes/stores at location on system.
'''
class QRBlueprint(object):

	def __init__(self, is_new=1, code_int=0):

		# Intialize QR class to use to encode
		self.QRCode = QR(code_int)
		self.base = None
		self.routing_code = None

	# Create_code will create a blueprint of a qr code pointing to the run-machine endpoint.
	# This class exists to make QR handling easier on the developer (Michael)
	def create_code(self):

		#self.base = (request.base_url).split('new-machine')[0]
		self.base = '127.0.0.1:5500/'

		# Create a QR code pointing to Run-machine front end
		self.QRCode.create_qr(self.base + 'Run-Machine.html?machine=')

		# Save to System
		self.routing_code = self.QRCode.save_qr()

		if self.routing_code == -1:
		 	return "ERROR, Please Refresh the Page and Try again"

		# Send the routing code back to the user
		return (self.routing_code + '.png')