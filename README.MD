### This program is a signal app chat bot.

It was written as a volunteer effort for fellow ICE watchers. The intention is to allow for members of a signal chat to snap a photo or manually enter in a licence plate number and for that value to be held in an SQLlite Database, locally.

Still obviously early in development, it does not quite do anything at this commit. I intend to use a photo reading library to read the license plate text from photos uploaded to the signal chat, which will download to the host PC where it'll be read by this program. It is intended for small scale use and each group should run it's own. Data transfer between instances may be considered in the future.

I will include a shellscript for an installation using signal-api to mimick the setup I am using. It will only work for linux operating systems.

### To install the chat bot:

To read the variables in config.yaml, we will use a tool called yq. Install it with

> sudo dnf install yq

or

> sudo apt install yq

Please have Python3 installed correctly.
Install the libraries this script uses. You can do so with:
> pip install asyncio, signalbot, logging, yaml, nest_asyncio

Rename or copy the file named config.example.yaml to be config.yaml and set the values inside to your values. Please note the area code is required for the phone number.
> signal_service: "http://localhost:8080"

> PHONE_NUMBER = +19100000000

You will need to install and use a the signal-cli, which can be downloaded [here](https://github.com/AsamK/signal-cli/releases/latest).
You will need the signal-cli-rest-api as well, but the download and installation is handled by dockerInit.sh

### To setup the chat bot:
Firstly, you'll want to connect the host device to your bot's account, or create a new account. Either way, you'll need a real phone number to maintain the account. I use singal-cli for this. Please see the [Quickstart guide for signal-api](https://github.com/AsamK/signal-cli/wiki/Quickstart).

I ended up linking my primary account to the new bot account. My android phone is my primary device, so linking this required taking the QR code link given by the signal-cli-rest-api website, which is (while the docker image is running) http://localhost:8080/v1/qrcodelink?device_name=signal-api and scanning it with Signal's mobile app. Look in Settings > Linked devices. To do this, you'll need to set up the docker image, which can be done using my dockerInit.sh script and then running the new docker image with dockerRun.sh

For usage after account is linked up, you'll need to run both programs: the docker image (with dockerRun.sh), and this program's "main.py"
You'll need two terminal and run one command in each:

> bash dockerRun.sh

> python3 main.py