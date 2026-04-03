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
    triggered,
    regex_triggered
)
import nest_asyncio
nest_asyncio.apply()

with open('config.yaml', 'r') as file:
    CONFIG = yaml.safe_load(file)
    file.close()

loggingLevel = CONFIG["LOGGING_LEVEL"] #Change in config.yaml options: DEBUG, INFO, ERROR, CRITICAL from most to least verbose/detailed
logging.basicConfig(
    level=str(f"{loggingLevel}"),
    format='%(asctime)s - %(levelname)s - %(message)s',
)

class Functions():
    dir = CONFIG["STORE_PATH"]

    connection = sqlite3.connect(dir)
    cursor = connection.cursor()

    def database_init():
        table = Functions.cursor.execute(f"SELECT * FROM IceWatch;")
        tables = Functions.cursor.fetchall()
        if tables is not None:
            return True
        else:
            Functions.cursor.execute("CREATE TABLE IceWatch LP, Heading, TimeReported")
            return True

    def database_retrieve(LP):
        Functions.database_init() #Makes sure DB/Table exists.
        time = ""
        place = ""
        try:
            Functions.cursor.execute("SELECT * FROM IceWatch WHERE LP = ?", (LP[0],))
            selection = Functions.cursor.fetchall()
            if selection is not None:
                return True
            else:
                return False
        except Exception as e:
            logging.error(f"Exception has occured, see\n{e}")
            return False
        finally:
            logging.debug(f"database_retrieve has finished\nArray 'LP' is: {LP}\nVariables 'time', 'place' is: {time}, {place}\n'selection' is {selection}")

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
        place = "" #placeholder for now
        data = str(c.message).replace("!LP", '').strip()
        data = data.split(', ', 1)
        time = datetime.datetime.now()
        time = time.strftime('%d/%m/%Y %H:%M')
        if len(data) == 1:
            exists = Functions.database_retrieve(data)
            logging.debug(f"exists, time, place is: {exists}, {time}, {place}")
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
    bot = SignalBot(
        Config(
            signal_service=CONFIG["SIGNAL_SERVICE"],
            phone_number=CONFIG["PHONE_NUMBER"]
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
        logging.error(f"An error occured. See: \n{e}")
    finally:
        #Close SQLite DB, if not already done
        if Functions.connection:
            Functions.cursor.close()
        exit()