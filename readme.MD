### This program is a signal app chatbot.

It was written as a volunteer effort for fellow ICE watchers. The intention is to allow for members of a signal chat to snap a photo or manually enter in a licence plate number and for that value to be appended to a CSV file.

Still obviously early in development, it does not quite do anything at this commit. I intend to use a photo reading library to read the license plate text from photos uploaded to the signal chat, which will download to the host PC where it'll be read by this program. It is intended for small scale use and each group should run it's own. Data transfer between instances may be considered in the future.

I will include a shellscript for an installation using signal-api to mimick the setup I am using. It will only work for linux operating systems.

### To install the bot:

Please have Python3 installed correctly.
Install the libraries this script. You can do so with:
> pip install asyncio, signalbot, logging

Create a text file named keys.py
Add these lines in that file as follows:
> SIGNAL_SERVICE = 123456789

> PHONE_NUMBER = 123456789

You will need to install and use a signal api, be it [signal-api](https://github.com/AsamK/signal-cli) or the dockerized [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api)

[Quickstart guide for signal-api](https://github.com/AsamK/signal-cli/wiki/Quickstart)

[Quickstart guide for signal-cli-rest-api](https://stefanstranger.github.io/2021/06/01/RunningSignalRESTAPIinAppService/) (This one is a blogpost by a Stefan Stranger)

### To use the bot:
First, run your signal API. I will be using signal-api

## Initializing the bot
I am learning how to do this as I make this document and will update it as I understand it better. It seems that signal doesn't have bot specific accounts so we must use a user account that is linked to a real phone number. For testing purposes I will be using my own cell phone. This means my personal account will be the bot's account, I recommend getting a cheap dedicated cell phone for this or some form of paid VOIP that the host machine can access. The bot won't need the phone while running, but the account's creation will need the phone.
It comes from a github repo called signal-cli, found here: https://github.com/AsamK/signal-cli

