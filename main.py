import asyncio
from keys import ACCOUNT_UUID
from signalbot import Command, Config, Context, SignalBot, enable_console_logging, triggered
import logging
import os

async def csv_function():
    pass

async def reply():
    try:
        csv_function()
    else:
        pass

    await signal.send_reaction(message, "🦀")
    await signal.send_message(context[1],"Sorry, just feeling a little crabby.")
    return True

async def test_command():
    @triggered("?LP")
    async def handle(self, c: Context) -> None:
        await c.send("Test Message")

async def main():
    enable_console_logging(logging.INFO)

    bot = SignalBot(
        Config(
            signal_service=os.environ["SIGNAL_SERVICE"],
            phone_number=os.environ["PHONE_NUMBER"],
        )
    )
    bot.register(test_command())  # Run the command for all contacts and groups
    bot.start()
