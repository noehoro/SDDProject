from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from time import sleep
import sys
import os

'''
Class SMS uses Twilio, an online web API to help implement SMS. Twilio is a paid service, so currently 
we don't have my client credentials here (developers paste in to run the code in development to keep my user
credentials from being stolen). SMS is designed to be used by the child process running on a seperate thread
in the CPU, using System time of that thread to tell how much time has passed (sleep), this allows our main
implementation to run in parallel to SMS, and we send any errors SMS has through a PIPE, routing STDOUT to the write
end of the pipe. SMS simply handles user notifications.
'''
class SMS:

	def __init__(self, number):
		# Setup twilio to be used by class, specify number to be used as sender
		self.client = Client('ACd6f8fa3555f40caef53a35bb1d9e3799', 'a669bab27a47bcf3f736c88a3b3b0ab2')
		self.number = number

	# send_start sends the starting message to the user, signaling a machine run
	def send_start(self, to_number):

		# Try to send a message to the client's number, on success, return true. On error, return false
		print(to_number)
		self.client.messages.create(to=to_number, from_=self.number, body="Your Laundry Machine has been started successfully! We will text you when it is complete!")
		return True


	# send_complete sends the completion message to the user, signaling a machine finish
	def send_complete(self, to_number):

		# Try to send a message to the client's number, on success, return true. On error, return false
		try:
			self.client.messages.create(to=to_number, from_=self.number, body="Your Laundry Machine is complete! Please navgiate to the Laundry Room to get your stuff out!")
		except:
			return False


# Driver code for Child process. This code is run when the thread is created, basically telling SMS
# what to do.
if __name__ == "__main__":

	SMS = SMS(number='+12058460434')
	SMS.send_start(sys.argv[1])
	sleep(int(sys.argv[2]))
	SMS.send_complete(sys.argv[1])