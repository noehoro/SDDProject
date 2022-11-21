# Laundry Manager API #
### By Michael Anderson ###

> Development Setup
>>> Requires Pip and Python3.8+
>> *First, clone the repository to your local system by using `git clone https://github.com/noehoro/SDDProject.git`
>> *Next, use `cd` to naviagate to the `backend` folder
>> *You can use Anaconda to set up a Development Environment, or, simply install the `requirements.txt` file by typing `pip install -r requirements.txt`
>> *Now, while in the `backend` folder, run `python3 app.py`, and the development server is running! To confirm, visit the link that is output by your terminal and you should see `{"title":"Laundry Manager","ver":"beta_v1.0"}`.

 Endpoint   |  Request Type  |  Arguments  |  Function  | Return Value
 ---------- | -------------- | ----------- | ---------- | ------------
 /register | POST | username, password, site_post | Registers a user's account | {exists: 1\| 0, success: 1\|0}
 /login | POST | username, password | Logs in the user. User's are remembered, adds login to user's cookie. | {loggedin: 1\|0, pass: 1\|0, user: 1\|0}
 /new-machine | POST | time, site, type:(wash, dry, or other) | Creates a new machine. Gives the user back an image of a QR code for that machine | Currently returns an image, however I'm willing to change this to a string specifying the path of the file.
/run-machine | POST | machine, number (format include country code, e.g. "+15063722738") | With the Machine's ID, the function queries the database and returns the time the machine takes. With phone number provided, it will send a intial text and a finishing text to # provided | {machine_time: int}
/logout | GET | None | Logs out the user, and removes log in boolean from their cookies. NOTE: If the user is not logged in, this endpoint will respond with an error! | {loggedout:1}
/dashboard | POST | site | Returns all the machine in the site and their time remaining. Machines are encoded by the following legend: 1: washer, 2: dryer, 3: other | Dict with keys as Machine ID and Value as Machine's remaining time NOTE: Machines not running with will have a time value of 0, and Machines that are BROKEN are will have a value of -1! Example: {11255234: 1435, 22332523: 0, 32332523: -1}.
/getsite | GET | None | Returns the user's site's name | {site: Stirng}
/createcode | POST, GET | machineid (optional) | Creates or gets a QR code, this endpoint isn't meant to be called by the user unless the user is trying to create a QR code for a machine that already exists. | {address: String pointing to file location of new image} 
/ | GET | None | Default endpoint, returns info on API (used mostly for testing) | {title: Laundry Manager, ver: beta_v1.0}
/loggedin | GET | None | Checks if a user is logged in or not | {loggedin: 1 if logged in, 0 if not}
/report | POST | machine | Given the machine ID, the machine will be marked as broken (-1 value from dashboard call) | {success: 1}
/fixed | POST | machine | Given the machine ID, the machine will be marked as NOT broken (fixed), means it will be able to be run and have a time value in dashboard call | {success: 1}
/changeusername | POST | newname | Given a new username (newname), the user's profile will lose its former username and gain the new one. | {success:1, success:0} NOTE: Success: 0 mean the username is taken!
/changepassword | POST | newpass | Given a new password (newpass), the user's profile will use newpass as its password instead on next login. | {success:1}


And more to come! I'm dilligently working on ironing out any issues with these endpoints, as well as implementing the SMS endpoints!
