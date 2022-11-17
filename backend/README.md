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
/run-machine | POST | machine | With the Machine's ID, the function queries the database and returns the time the machine takes. | {machine_time: int}
/logout | GET | None | Logs out the user, and removes log in boolean from their cookies. NOTE: If the user is not logged in, this endpoint will respond with an error! | {loggedout:1}
/dashboard | POST | site | Returns all the machine in the site and their time remaining. Machines are encoded by the following legend: 1: washer, 2: dryer, 3: other | Dict with keys as Machine ID and Value as Machine's remaining time NOTE: Machines not running with will have a time value of 0! Example: {11255234: 1435, 22332523: 0}.
/getsite | GET | None | Returns the user's site's name | {site: Stirng}
/createcode | POST, GET | machineid (optional) | Creates or gets a QR code, this endpoint isn't meant to be called by the user unless the user is trying to create a QR code for a machine that already exists. | {address: String pointing to file location of new image} 
/ | GET | None | Default endpoint, returns info on API (used mostly for testing) | {title: Laundry Manager, ver: beta_v1.0}
/loggedin | GET | None | Checks if a user is logged in or not | {loggedin: 1 if logged in, 0 if not}
And more to come! I'm dilligently working on ironing out any issues with these endpoints, as well as implementing the SMS endpoints!
