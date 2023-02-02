import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """_Start function from project"""
    await update.message.reply_text(
        "Hello there, My name is FolzeckGroup Bot, type /help to open the functionalities of our system"
    )

def main() -> None:
    """Run the bot."""
    app = (
        Application.builder()
        .token("5890227974:AAFI_vdRD7GXSE3Iy4aiE6GF6vFAhMt_J3w")
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    
    reply_help=[["/start", "/help", "/create"]]
    
    await update.message.reply_text("""
    The following commands are available:
    
    /start -> Welcome to the channel)
    /help -> This message
    /create -> Create New User 

    """,
    reply_markup=ReplyKeyboardMarkup(
            reply_help, one_time_keyboards=True, input_field_placeholder="Choose one")

     )
