import asyncio
import sqlite3
import yaml
import logging
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

class TestCommand():
    try:
        Functions.csv_function()
    except:
        pass

class PingCommand(Command):
    @triggered("Ping")
    async def handle(self, c: Context) -> None:
        await c.send("Pong")

def main():
    enable_console_logging(logging.INFO)
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    bot = SignalBot(
        Config(
            signal_service=config["signal_service"],
            phone_number=config["phone_number"],
        )
    )

    bot.register(PingCommand(), contacts=False, groups=True)
    bot.start()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occured. See: \n", e)
    finally:
        exit()