import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from apis import meteoAPI, jokeAPI, apodAPI
from csv_json import csv_json
from scraping import periodico, cartelera
from sql import inferno

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

async def handle_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.document)
    filepath = "downloads/" + update.message.document.file_name
    await file.download_to_drive(filepath)

    df = csv_json.convert_to_dataframe(filepath)
    columnas, estadisticas = csv_json.get_csv_info(df)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=columnas)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=estadisticas)

    archivo_json = csv_json.csv_to_json(df, filepath)
    await context.bot.send_document(chat_id=update.effective_chat.id, document=open(archivo_json, "rb"))

    os.remove(filepath)
    os.remove(archivo_json)

async def handle_json(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.document)
    filepath = "downloads/" + update.message.document.file_name
    await file.download_to_drive(filepath)
    
    df = csv_json.convert_to_dataframe(filepath)

    archivo_csv = csv_json.json_to_csv(df, filepath)
    await context.bot.send_document(chat_id=update.effective_chat.id, document=open(archivo_csv, "rb"))

    os.remove(filepath)
    os.remove(archivo_csv)
    
async def handle_noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    portada = periodico.scrapping_periodico()
    for noticia in portada:
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text=f"{noticia['titular']}\n{noticia['enlace']}")

async def handle_peliculas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    peliculas_hoy = cartelera.scrapping_periodico()
    for pelicula in peliculas_hoy:
        await context.bot.send_photo(chat_id=update.effective_chat.id,
                                     photo=pelicula["imagen"],
                                     caption=f"{pelicula['titulo']}\n{pelicula['enlace']}")

async def handle_inferno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    condena = inferno.chamando_a_satanas()
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text=f"Nombre: {condena[1]}\nNivel: {condena[2]}\nPecado: {condena[3]}")

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

    noticias_handler = CommandHandler('noticias', handle_noticias)
    application.add_handler(noticias_handler)

    peliculas_handler = CommandHandler('peliculas', handle_peliculas)
    application.add_handler(peliculas_handler)

    inferno_handler = CommandHandler('inferno', handle_inferno)
    application.add_handler(inferno_handler)

    csv_handler = MessageHandler(filters.Document.FileExtension("csv"), handle_csv)
    application.add_handler(csv_handler)

    json_handler = MessageHandler(filters.Document.FileExtension("json"), handle_json)
    application.add_handler(json_handler)

    # Keeps the application running
    application.run_polling()