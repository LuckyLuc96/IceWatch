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
    sqlite_path = CONFIG["STORE_PATH"]

    connection = sqlite3.connect(sqlite_path)
    cursor = connection.cursor()

    def database_init():
        table = Functions.cursor.execute(f"SELECT * FROM IceWatch;")
        tables = Functions.cursor.fetchall()
        if tables is not None:
            return True
        else:
            Functions.cursor.execute("CREATE TABLE IceWatch LP, Heading, TimeReported")
            return True

    def database_retrieve(data):
        Functions.database_init() #Makes sure DB/Table exists.
        try:
            Functions.cursor.execute("SELECT * FROM IceWatch WHERE LP=?", (data,))
            selection = Functions.cursor.fetchall()
            newList = []
            for tup in selection:
                newList.append(tup)
            if newList:
                logging.debug(f"'newSelection[-1]' is {newList[-1]}")
                return True, newList[-1]
            else:
                selection = ""
                return False, selection
        except Exception as e:
            logging.error(f"Exception has occured, see\n{e}")
            selection = ""
            return False, selection
        finally:
            logging.debug(f"database_retrieve has finished")

    def database_store(data, time):
        try:
            Functions.cursor.execute(f"INSERT INTO IceWatch VALUES (?, ?, ?);", (data[0], data[1], time))
            Functions.connection.commit()
            return True
        except Exception as e:
            logging.critical(f"Something has gone very wrong here. See: {e}")
            return False
        return False

    def get_img_datetimes():
        dir = r"signal-cli-config/attachments"
        for file in os.scandir(dir):
            time = os.path.getctime(file)
            logging.debug(f"file is: {file} - time is: {time}")
        logging.debug("'get_img_datetimes' has finished running.")

class LicensePlateCommand(Command):
    table = bool
    @regex_triggered("!LP")
    async def handle(self, c: Context) -> None:
        place = "" #placeholder for now
        data = str(c.message).replace("!LP", '').strip()
        data = data.split(', ', 1)
        time = datetime.datetime.now()
        time = time.strftime('%H:%M on %d/%m/%Y')
        chars = 0
        for character in data[0]: #Count characters in License plate input and make sure they meet a critera
            chars = chars + 1
        datachars = chars
        if datachars > 9 or datachars < 3:
            await c.send("Please check the license plate entered for correctness.")
            return
        if len(data) == 1: #Query command
            data = str(data[0])
            exists, selection = Functions.database_retrieve(data)
            if exists == True:
                logging.debug(f"exists = {exists} and selection = {selection}")
                await c.send(f"LP: '{data}' last reported: {selection[2]}, with the heading: '{selection[1]}'.")
            if exists == False:
                logging.debug(f"exists = {exists} and selection = {selection}")
                await c.send(f"LP '{data}' has not been recorded before. Please repeat the command and include a current location and heading. The time will automatically be recorded when you send the message. Example: '!LP PH1000, On market street and 13th street going north'")
        if len(data) == 2: #Update/Input command
            success = Functions.database_store(data, time)
            if success == True:
                await c.send(f"License Plate number '{data[0]}' has sucessfully been recorded going '{data[1]}' at {time}")
            if success == False:
                await c.send(f"An error occured with the bot. Please contact the operator. The license plate {data[0]} has not been recorded at this time.")
                logging.error(f"An error occured with the recording of '{data[0]}' by user [placeholder]. The input collected was:\n{data}")

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