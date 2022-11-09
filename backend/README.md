# Laundry Manager API #
### By Michael Anderson ###

> Development Setup
>>> Requires Pip and Python3.8+
>> First, clone the repository to your local system by using `git clone https://github.com/noehoro/SDDProject.git`
>> Next, use `cd` to naviagate to the `backend` folder
>> You can use Anaconda to set up a Development Environment, or, simply install the `requirements.txt` file by typing `pip install -r requirements.txt`
>> Now, while in the `backend` folder, run `python3 app.py`, and the development server is running! To confirm, visit the link that is output by your terminal and you should see `{"title":"Laundry Manager","ver":"beta_v1.0"}`.

 Endpoint   |  Request Type  |  Arguments  |  Function  | Return Value
 ---------- | -------------- | ----------- | ---------- | ------------
 /register | POST | username, password, site_post | Registers a user's account | {exists: 1\| 0, success: 1\0}
 /login | POST | username, password | Logs in the user. User's are remembered, adds login to user's cookie. | {loggedin: 1|0, pass: 1|0, user: 1|0}
 /new-machine | POST | time, site | Creates a new machine. Gives the user back an image of a QR code for that machine | Currently returns an image, however I'm willing to change this to a string specifying the path of the file.

