import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from apis import meteoAPI, jokeAPI, apodAPI

load_dotenv()
# Authentication to manage the bot
TOKEN = os.getenv('TOKEN')

# Show logs in terminal
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# This function responds to start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Son un bot, dime algo!")

async def tiempo_api(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tiempo = meteoAPI.extract_info(meteoAPI.load_json())
    await context.bot.send_message(chat_id=update.effective_chat.id, text=tiempo["title"]+":")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=tiempo["hoy"])
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Cielo: " + tiempo["cielo"])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Temperatura máxima: {tiempo['temp_max']}ºC\n"+
                                                                          f"Temperatura mínima: {tiempo['temp_min']}ºC")
    
async def chiste_api(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chiste = jokeAPI.extract_info(jokeAPI.load_json())
    await context.bot.send_message(chat_id=update.effective_chat.id, text=chiste["chiste"])

async def apod_api(update: Update, context: ContextTypes.DEFAULT_TYPE):
    apod = apodAPI.extract_info(apodAPI.load_json(apodAPI.get_apikey()))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=apod["title"])
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=apod["imagen"])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=apod["descripcion"])

if __name__ == '__main__':
    # Start the application to operate the bot
    application = ApplicationBuilder().token(TOKEN).build()

    # Handler to manage the start command
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    tiempo_handler = CommandHandler('tiempo', tiempo_api)
    application.add_handler(tiempo_handler)

    chiste_handler = CommandHandler('chiste', chiste_api)
    application.add_handler(chiste_handler)

    apod_handler = CommandHandler('apod', apod_api)
    application.add_handler(apod_handler)

    # Keeps the application running
    application.run_polling()