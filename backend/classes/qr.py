import qrcode
import random as rand

'''
Class QR implements QRCODE python module, and creates codes pertaining 
to our laundry machines. 
'''
class QR:

	# Constructor stores code given 
	def __init__(self, code: int):

		self.code = code 
		self.code_image = None

	# create_qr does just that, makes a qr image and stores the the image attribute. Takes ep, which is just
	# the Extra Positional number that specifies wheteher a machine is wash, dry, etc.
	def create_qr(self, ep: str) -> str:

		self.code_image = qrcode.make(str(ep) + str(self.code))
		return str(ep)+str(self.code_image)

	# Saves QR code to system, tells caller where the qr code is saved. Files are generated with a random number
	# id attached to prevent overwrites
	def save_qr(self):

		# Produce random id
		temp_code_num = rand.sample(range(1, 10000), 1)[0] 

		# Make sure image exists
		if self.code_image == None:
			return -1

		# Name and save qr image
		self.code_image.save('qr_'+ str(temp_code_num) + '.svg')

		# Tell Caller name of image file
		return 'qr_' + str(temp_code_num)




