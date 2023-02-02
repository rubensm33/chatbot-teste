import logging
from telegram import Update
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
