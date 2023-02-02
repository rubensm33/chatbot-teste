
"""
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ApplicationBuilder, Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler,filters


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)

#Start function 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:

    await update.message.reply_text(

        "Hello there, My name is FolzeckGroup Bot, type /help to open the functionalities of our system"

        )

def main() -> None:
    """Run the bot."""

    # Creation of the Application and pass bot's token.

    app = Application.builder().token("5890227974:AAFI_vdRD7GXSE3Iy4aiE6GF6vFAhMt_J3w").build()

    app.add_handler(

        CommandHandler("start", start)

    )

    #Run the application until the user press CTRL + C

    app.run_polling()


if __name__ == "__main__":
    main()



    