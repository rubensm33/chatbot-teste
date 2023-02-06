from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import httpx

NAME, LASTNAME, AGE, GENRE, RETRIEVE = range(5)


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """_Start function from project"""
    await update.message.reply_text(
        "Hello there, My name is FolzeckGroup Bot, type /help to open the functionalities of our system"
    )


async def help(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Iniciate help offering the options below to select"""

    reply_help = [["/start", "/help", "/create", "/retrieve"]]

    await update.message.reply_text(
        """
        
    The following commands are available:\n\n
    
    /start -> Welcome to the channel\n
    /help -> This message\n
    /create -> Create New User\n
    /retrieve -> Retrieve all users\n

    """,
        reply_markup=ReplyKeyboardMarkup(
            reply_help, input_field_placeholder="Choose one"
        ),
    )


async def create(update: Update, _: ContextTypes.DEFAULT_TYPE) -> NAME:
    """Iniciate creation user and ask for name

    Returns:
        NAME: name state
    """
    await update.message.reply_text(
        "Welcome to the function create user.\n"
        "Send /cancel to stop talking to me.\n\n"
        "To start type your name below",
    )
    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> LASTNAME:
    """Save name and ask for lastname

    Returns:
        LASTNAME: lastname state
    """
    context.user_data["name"] = update.message.text
    await update.message.reply_text("And about your last name?")
    return LASTNAME


async def lastname(update: Update, _: ContextTypes.DEFAULT_TYPE) -> AGE:
    """Save lastname and ask for age

    Returns:
        AGE: age state
    """
    _.user_data["lastname"] = update.message.text
    await update.message.reply_text(
        "In order for us to proceed with your service, please enter your age."
    )
    return AGE


async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> GENRE:
    """_Save age and ask for genre

    Returns:
        GENRE: genre state
    """
    context.user_data["age"] = update.message.text
    reply_keyboard = [["Male", "Female"]]
    await update.message.reply_text(
        "Are you a Male or Female?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Male or Female?",
        ),
    )
    return GENRE


async def genre(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> ConversationHandler:
    """Save genre and finish create user

    Returns:
        ConversationHandler: end create
    """
    context.user_data["genre"] = update.message.text
    await update.message.reply_text(
        "Thanks!!! Your user has been registered. See you later."
    )
    post_user = httpx.post("http://127.0.0.1:8000/add-user", json=context.user_data)
    return ConversationHandler.END


async def cancel(update: Update, _: ContextTypes.DEFAULT_TYPE) -> ConversationHandler:
    """Cancel create user

    Returns:
        ConversationHandler: cancel create
    """
    await update.message.reply_text(
        "The operation will be canceled", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


async def retrieve(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Retrive user

    Returns
        ConversationHandler: retrieve user"""
    retrieve_users = httpx.get("http://127.0.0.1:8000/list-users")
    dict_format = "Name: {name}\nLastname: {lastname}\nAge: {age}\nGenre: {genre}"

    users = "".join(
        [dict_format.format_map(user) + "\n" for user in retrieve_users.json()]
    )
    await update.message.reply_text(f"These are all users\n\n{users}")

    return ConversationHandler.END


async def retrieve_by_index(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Retrieve by Index

    Returns:
        RETRIEVE: Retrieve state
    """
    await update.message.reply_text("Select an user by Index")
    return RETRIEVE


async def return_retrieve(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Retrieve by Index

    Returns:
        ConversationHandler: retrieve user
    """
    reply_user = update.message.text
    retrieve_user = httpx.get(f"http://127.0.0.1:8000/list-user-by-index/{reply_user}")
    await update.message.reply_text(
        f"These are the user selected\n\n{retrieve_user.text}"
    )
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    app = (
        ApplicationBuilder()
        .token("5890227974:AAFI_vdRD7GXSE3Iy4aiE6GF6vFAhMt_J3w")
        .build()
    )
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("create", create)],
        states={
            NAME: [MessageHandler(filters.TEXT, name)],
            LASTNAME: [MessageHandler(filters.TEXT, lastname)],
            AGE: [MessageHandler(filters.TEXT, age)],
            GENRE: [MessageHandler(filters.TEXT, genre)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    conv_retrieve = ConversationHandler(
        entry_points=[CommandHandler("retrieve_by_index", retrieve_by_index)],
        states={
            RETRIEVE: [MessageHandler(filters.TEXT, return_retrieve)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("retrieve", retrieve))
    app.add_handler(conv_retrieve)
    app.run_polling()


if __name__ == "__main__":
    main()
