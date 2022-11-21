from twilio.rest import Client
from time import sleep
import sys

class SMS:

	def __init__(self, number):

		self.client = # blank as to not expose account credentials
		self.number = number

	def send_start(self, to_number):
		try:
			self.client.messages.create(to=to_number, from_=self.number, body="Your Laundry Machine has been started successfully! We will text you when it is complete!")
			return True
		except: 
			return False

	def send_complete(self, to_number):
		try:
			self.client.messages.create(to=to_number, from_=self.number, body="Your Laundry Machine is complete! Please navgiate to the Laundry Room to get your stuff out!")
		except:
			return False


if __name__ == "__main__":

	SMS = SMS(number='+12058460434')
	SMS.send_start(sys.argv[1])
	sleep(int(sys.argv[2]))
	SMS.send_complete(sys.argv[1])