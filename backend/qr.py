import qrcode
import random as rand

class QR:
	def __init__(self, code: int):

		self.code = code 
		self.code_image = None

	def create_qr(self, data: int, ep: str):

		self.code_image = qrcode.make(ep + data + self.code)
		return code_image

	def save_qr(self):

		temp_code_num = rand.sample(range(1, 10000), 1) 

		if self.code_image == None:
			return -1
		elif self.code_image.save('qr_'+ str(temp)) < 0:
			return -1

		return 'qr_' + str(temp_code_num)





