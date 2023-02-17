import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from telegram.ext.filters import BaseFilter
from dotenv import load_dotenv
from rapaygo import create_invoice
import os 

#local imports
from gpt import generate_text

load_dotenv()

# Set up your Telegram bot token here
token=os.getenv("TOKEN")
bot = telegram.Bot(token)

# Define the function that will handle the '/start' command
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hello! I'm a bot. How can I help you?")

# Define the function that will handle user messages
def respond(update, context):
    user_message = update.message.text
    context.bot.send_message(chat_id=update.message.chat_id, text=f"You said: {user_message}")

# Define a handler function to handle the /prompt command
def handle_prompt(update, context):
    # Read the text after the command
    prompt_text = ' '.join(context.args)
    # Do something with the prompt_text
    # For example, send a response back to the user
    update.message.reply_text('You asked: "' + prompt_text + '" Send me sats first and I will answer!')
    create_invoice()
    invoice=create_invoice()
    # Load the image file
    with open('invoice.png', 'rb') as f:
        photo = f.read()
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=invoice)
    #message = generate_text(prompt_text)
    #context.bot.send_message(chat_id=update.message.chat_id, text=f"This is the message: {message}")

# Set up the CommandHandler and MessageHandler for your bot
updater = Updater(bot=bot, persistence=None, use_context=True)
dispatcher = updater.dispatcher


    

# Add the handler function to the dispatcher
updater.dispatcher.add_handler(CommandHandler('prompt', handle_prompt))

start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text & (~Filters.command), respond)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()