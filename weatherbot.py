import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os

# Konfigurasi logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# API Token dari BotFather
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '7541468356:AAHFE3KcR9wWqtWqb6o2rCfd6uLl4Wvw4bU')

# OpenWeatherMap API Key
WEATHER_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY', '1d738f51eac14836efa33bf9416502a5')

# Fungsi untuk menghandle perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Selamat datang! Saya adalah bot cuaca. Ketik /help untuk melihat perintah yang tersedia.")

# Fungsi untuk menghandle perintah /help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Perintah yang tersedia:\n- /cuaca <kota> untuk melihat cuaca saat ini")

# Fungsi untuk menghandle perintah /cuaca
async def cuaca(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Silakan masukkan nama kota. Contoh: /cuaca Jakarta")
        return

    kota = " ".join(context.args)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={kota}&appid={WEATHER_API_KEY}&units=metric&lang=id"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        cuaca = data["weather"][0]["description"]
        suhu = data["main"]["temp"]
        kelembaban = data["main"]["humidity"]
        kecepatan_angin = data["wind"]["speed"]
        
        pesan = (
            f"Cuaca di {kota}:\n"
            f"• Kondisi: {cuaca}\n"
            f"• Suhu: {suhu:.1f}°C\n"
            f"• Kelembaban: {kelembaban}%\n"
            f"• Kecepatan angin: {kecepatan_angin} m/s"
        )
        
        await update.message.reply_text(pesan)
    except requests.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        await update.message.reply_text("Gagal mengambil data cuaca. Silakan coba lagi nanti atau periksa nama kota.")

# Fungsi untuk menghandle pesan yang tidak dikenal
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Perintah tidak dikenal. Ketik /help untuk melihat perintah yang tersedia.")

def main() -> None:
    # Membuat aplikasi Telegram bot
    application = Application.builder().token(TOKEN).build()

    # Mengatur handler untuk perintah /start
    application.add_handler(CommandHandler("start", start))

    # Mengatur handler untuk perintah /help
    application.add_handler(CommandHandler("help", help))

    # Mengatur handler untuk perintah /cuaca
    application.add_handler(CommandHandler("cuaca", cuaca))

    # Mengatur handler untuk pesan yang tidak dikenal
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Menjalankan aplikasi Telegram bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()