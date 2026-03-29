import asyncio
import sqlite3
import yaml
import logging
import os
from signalbot import (
    Command,
    Config,
    Context,
    SignalBot,
    enable_console_logging,
    triggered
)
import nest_asyncio
nest_asyncio.apply()

class Functions():
    def csv_function():
        pass
    def database_store():
        pass
    def database_retrieve():
        pass
    def get_img_datetimes():
        dir = r"signal-cli-config/attachments"
        for file in os.scandir(dir):
            time = os.path.getctime(file)
            print(file, time)

class TestCommand():
    try:
        Functions.csv_function()
    except:
        pass

class LicensePlateCommand(Command):
    @triggered("!LP" or "!lp" or "!Lp")
    async def handle(self, c: Context) -> None:
        await c.send(str(c.message))

class HelpCommand(Command):
    @triggered("!Help" or "!HELP" or "!help")
    async def handle(self, c: Context) -> None:
        await c.send("The existing commands can be called with !Help or !LP (short for License Plate")
        await c.send("The Help Command shows this message. The LP command is being built to do various commands based on existing data or newly imported images/data. More to come.")

def main():
    enable_console_logging(logging.DEBUG)
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    bot = SignalBot(
        Config(
            signal_service=config["SIGNAL_SERVICE"],
            phone_number=config["PHONE_NUMBER"],
            storage=config["STORAGE"]
        )
    )

    bot.register(LicensePlateCommand(), contacts=False, groups=True)
    bot.register(HelpCommand(), contacts=False, groups=True)
    #bot.register(TestCommand(), contacts=True, groups=True)
    bot.start()

if __name__ == "__main__":
    #main()
    try:
        main()
    except Exception as e:
        print(f"An error occured. See: \n", e)
    finally:
        exit()