### This program is a signal app chat bot.

It was written as a volunteer effort for fellow ICE watchers. The intention is to allow for members of a signal chat to snap a photo or manually enter in a licence plate number and for that value to be held in an SQLite3 Database, locally.

## WORKING

* Storing data remotely using the Signal App

* Retrieving the last column of data entered for any one license plate

* Check if a License Plate number has already been entered. (Redudant?) Data isn't over written, but added when a license plate is entered, so this command may be combined later

## TODO

* Read a plate off of a clear image and enter it to the DB. Potentially, taking the meta data from that photo to get the location. Many phones and perhaps Signal itself may strip meta data, so that might not be available.

* Better commands. The method to input data is a strict format currently.

* Data transfer between instances via import/export

* Exporting the database via chat commands into a friendly format

* Deletion by admins of mistaken data

## User guide

There are 3 commands, one of them using the same keyword, but it does different things based on your input.

### !Help<br>
This display a help message to explain the other command.


### !LP LicensePlate#<br>
This will display the last entry for this licenseplate, if it exists.


### !LP LicensePlate#, Where the vehicle is at or heading<br>
This will enter in a new entry and automatically generate a time stamp.

### To install the chat bot:

To read the variables in config.yaml, we will use a tool called yq. Install it with

> sudo dnf install yq

replace dnf with whatever software manager you use.

Please have Python3 installed correctly.
Install the libraries this script uses. You can do so with:
> pip install asyncio, sqlite3, yaml, logging, os, datetime, signalbot, nest_asyncio

Rename or copy the file named config.example.yaml to be config.yaml and set the values inside to your values. Please note the area code is required for the phone number. The dockerInit script also create this file for you.

You will need the signal-cli-rest-api, but the download and installation is handled by dockerInit.sh

### To setup the chat bot:
After running dockerInit.sh, run dockerRun.sh and go to [this URL](http://127.0.0.1:8080/v1/qrcodelink?device_name=local) and connect your host device to your signal account.

I ended up linking my primary account to the new bot account. Look in Settings > Linked devices.

After the device is connected, restart the docker image by ending the process (control and C) and rerunning it.

<br>

### Turning it on:

For usage after account is linked up, you'll need to run both programs: the docker image (with dockerRun.sh), and this program's "main.py"
You'll need two terminal and run one command in each:

./dockerRun.sh

python3 main.py

