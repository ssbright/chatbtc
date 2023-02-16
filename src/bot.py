import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from telegram.ext.filters import BaseFilter
from dotenv import load_dotenv
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

# Define the handler function for the /prompt command
def prompt_handler(update, context):
    # Get the text following the /prompt command
    prompt_text = ' '.join(context.args)
    # Do something with the prompt_text
    # For example, you can store it in a variable, or use it to generate a response using the OpenAI API
    print("Received prompt:", prompt_text)
    context.bot.send_message(chat_id=update.message.chat_id, text=f"This is what you want me to ask chatgpt?: {prompt_text}")



# Set up the CommandHandler and MessageHandler for your bot
updater = Updater(bot=bot, persistence=None, use_context=True)
dispatcher = updater.dispatcher

# Define a handler function to handle the /prompt command
def handle_prompt(update, context):
    # Read the text after the command
    prompt_text = ' '.join(context.args)
    # Do something with the prompt_text
    # For example, send a response back to the user
    update.message.reply_text('You asked: "' + prompt_text + '" Send me sats first and I will answer!')
    message = generate_text(prompt_text)
    context.bot.send_message(chat_id=update.message.chat_id, text=f"This is the message: {message}")

    

# Add the handler function to the dispatcher
updater.dispatcher.add_handler(CommandHandler('prompt', handle_prompt))

start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text & (~Filters.command), respond)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()