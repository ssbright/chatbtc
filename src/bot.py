import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from telegram.ext.filters import BaseFilter
from dotenv import load_dotenv
from rapaygo import create_invoice, payment_confirmed_checker
import os 
import time

#local imports
from gpt import generate_text

load_dotenv()

# Set up your Telegram bot token here
token=os.getenv("TOKEN")
bot = telegram.Bot(token)

# Define the function that will handle the '/start' command
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hello! I'm a bot. How can I help you?")

def help(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Want to ask me a question? Start your questions with '/prompt' followed by whatever you want to ask!")

# Define the function that will handle user messages
def respond(update, context):
    user_message = update.message.text
    context.bot.send_message(chat_id=update.message.chat_id, text=f"You said: {user_message}")

# Define the function that waits for payment confirmation
def wait_for_payment_confirmation(pay_hash, amt):
    # wait for payment confirmation
    for i in range(600):
        time.sleep(1)
        # check if payment has been confirmed
        # if payment is confirmed, set confirmation to True and exit loop
        if payment_confirmed_checker(pay_hash, amt) == "COMPLETED":
            #status=payment_confirmed_checker(pay_hash, amt) == "COMPLETED"
            break

# Define a handler function to handle the /prompt command
def handle_prompt(update, context):
    # Read the text after the command
    prompt_text = ' '.join(context.args)
    # Do something with the prompt_text
    # For example, send a response back to the user
    update.message.reply_text('You asked: "' + prompt_text + '" Send me sats first and I will answer!')
    tokenDict=create_invoice()
    invoice="Here is your payment request for {} sats".format(tokenDict["amount"])
    # Load the image file
    with open('invoice.png', 'rb') as f:
        photo = f.read()
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=invoice)
    update.message.reply_text('{}'.format(tokenDict["payment_request"]))
    pay_hash=tokenDict["payment_hash"]
    wait_for_payment_confirmation(pay_hash, tokenDict["amount"])
    message = generate_text(prompt_text)
    context.bot.send_message(chat_id=update.message.chat_id, text=f"This is the message: {message}")


try: 
    # Set up the CommandHandler and MessageHandler for your bot
    updater = Updater(bot=bot, persistence=None, use_context=True)
    dispatcher = updater.dispatcher
        
    # Add the handler function to the dispatcher
    updater.dispatcher.add_handler(CommandHandler('prompt', handle_prompt))

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    message_handler = MessageHandler(Filters.text & (~Filters.command), respond)


    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(message_handler)

    # Start the bot
    updater.start_polling()
except Exception as e:
    print(f"Error:{e}")