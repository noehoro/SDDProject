import qrcode
import random as rand

class QR:
	def __init__(self, code: int):

		self.code = code 
		self.code_image = None

	def create_qr(self, ep: str) -> str:

		self.code_image = qrcode.make(str(ep) + str(self.code))
		return str(ep)+str(self.code_image)

	def save_qr(self):

		temp_code_num = rand.sample(range(1, 10000), 1)[0] 

		print("TEMP CODE NUM:", temp_code_num)
		print(self.code_image)

		if self.code_image == None:
			return -1

		self.code_image.save('qr_'+ str(temp_code_num) + '.png')

		return 'qr_' + str(temp_code_num)




