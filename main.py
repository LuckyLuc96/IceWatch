import asyncio
import sqlite3
import yaml
import logging
import os
import datetime
from signalbot import (
    Command,
    Config,
    Context,
    SignalBot,
    enable_console_logging,
    triggered,
    regex_triggered
)
import nest_asyncio
nest_asyncio.apply()

class Functions():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        file.close()

    dir = config["STORE_PATH"]

    connection = sqlite3.connect(dir)
    cursor = connection.cursor()

    def database_init():
        table = Functions.cursor.execute(f"SELECT * FROM IceWatch;")
        tables = Functions.cursor.fetchall()
        print(table, tables)
        if tables is not None:
            return True
        else:
            Functions.cursor.execute("CREATE TABLE IceWatch LP, Heading, TimeReported")
            return True

    def database_retrieve(LP):
        Functions.database_init() #Makes sure DB/Table exists.
        try:
            Functions.cursor.execute("SELECT * FROM IceWatch WHERE LP = ?", (LP,))
            selection = Functions.cursor.fetchall()
            return True, selection
        except Exception as e:
            print(f"Exception has occured, see\n{e}")
            return False, None
        finally:
            print(f"DEBUG: database_retrieve has finished\nLP is {LP},\nLP[0] is {LP[0]}")

    def database_store():
        pass

    def get_img_datetimes():
        dir = r"signal-cli-config/attachments"
        for file in os.scandir(dir):
            time = os.path.getctime(file)
            print(file, time)

class LicensePlateCommand(Command):
    table = bool
    @regex_triggered("!LP")
    async def handle(self, c: Context) -> None:
        data = str(c.message).replace("!LP", '').strip()
        data = data.split(', ', 1)
        time = datetime.datetime.now()
        time = time.strftime('%d/%m/%Y %H:%M')
        print(f"Post time.append{data}")
        if len(data) == 1:
            print(data)
            exists, result = Functions.database_retrieve(data)
            print(exists, result)
            if exists == True:
                await c.send(f"{data[0]} is has previously been recorded at {time} and {place}. If you would like to update the location, please run the command again, but this time add the new location/heading. The time will record automatically.")
            if exists == False:
                await c.send(f"{data[0]} has not been recorded before. Please repeat the command and include a current location and heading. The time will automatically be recorded when you send the message.")

class EchoCommand(Command):
    @regex_triggered("!echo")
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
        file.close()

    bot = SignalBot(
        Config(
            signal_service=config["SIGNAL_SERVICE"],
            phone_number=config["PHONE_NUMBER"]
        )
    )
    bot.register(LicensePlateCommand(), contacts=False, groups=True)
    bot.register(EchoCommand(), contacts=False, groups=True)
    bot.register(HelpCommand(), contacts=False, groups=True)
    #bot.register(TestCommand(), contacts=True, groups=True)
    bot.start()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occured. See: \n", e)
    finally:
        #Close SQLite DB and .yaml files
        if Functions.connection:
            Functions.cursor.close()
        if Functions.file:
            Functions.file.close()
        exit()