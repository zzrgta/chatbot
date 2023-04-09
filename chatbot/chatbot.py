from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext

import configparser
import logging
import pymysql

global db
global isTravel
global isAnswer


def main():
    global isTravel
    global isAnswer
    isTravel = False
    isAnswer = False
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    global db
    try:
        db = pymysql.connect(host="127.0.0.1", user="root" , password="zzr//2418gta", port=3306, db="botdb", charset="utf8")
        print('Success!')
    except:
        print('Lose connection!')
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("stop", stop))
    dispatcher.add_handler(CommandHandler("travel", travel))

    # To start the bot:
    updater.start_polling()
    updater.idle()

def echo(update, context):
    reply_message = update.message.text
    print("------------")
    print(reply_message)
    if isTravel == False:
        reply = 'I am so sorry that I cannot understand you. You can use "/travel" to launch travel guide.'
        logging.info("Update: " + str(update))
        logging.info("context: " + str(context))
        print(reply_message)
        context.bot.send_message(chat_id=update.effective_chat.id, text= reply)
    else:
        logging.info("Update: " + str(update))
        logging.info("context: " + str(context))
        global db
        cursor = db.cursor()
        msg = reply_message.split()
        print("++++++++++")
        print(msg)
        text1 = None
        text2 = None
        for i in list(msg):
            text2 = text1
            text1 = i
            if text2 == 'Hong' and text1 == 'Kong':
                print('=======')
                i = text2 + ' ' + text1
            sql = "select link from videos where city = '" + i + "'"
            print(sql)
            cursor.execute(sql)
            results = cursor.fetchone()
            print(results)
            if results != None:
                global isAnswer
                isAnswer = True
                link = "".join(results)
                update.message.reply_text("I found some information for the city you asked, you can watch the video: " + link)
        if isAnswer == False:
            reply = 'I am so sorry that I cannot understand you. I will collect the information to keep learning!'
            update.message.reply_text(reply)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def travel(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /travel is issued."""
    global isTravel
    isTravel = True
    update.message.reply_text('Hi! I am your travel guide, where would you like to travel? I can help you!')

def stop(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /stop is issued."""
    global isTravel
    isTravel = False
    update.message.reply_text('Thanks for using travel guide, see you next time!')

if __name__ == '__main__':
    main()
