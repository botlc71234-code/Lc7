import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

# Função do comando /start (A mensagem da sua foto)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 SEJA BEM-VINDO A OROCHI_STORE AS MELHORES FULL DADOS ESTAO AQUI 🚀\n"
        "✅ MATERIAL 100% VIRGEM✅\n"
        "📊 MATERIAL PREMIUM DE ADMIN FULL DADOS..."
    )
    
    # Criando os botões (Menu, Perfil, etc)
    keyboard = [
        [InlineKeyboardButton("Menu", callback_data='menu'), 
         InlineKeyboardButton("💎 Seu Perfil", callback_data='perfil')],
        [InlineKeyboardButton("🛠 SUPORTE", callback_data='suporte')],
        [InlineKeyboardButton("⚠️ REGRAS DE TROCA⚠️", callback_data='regras')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)

# Lógica para gerenciar os cliques nos botões
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'menu':
        await query.edit_message_text("Aqui está nosso menu de produtos...")
    # Adicione aqui os outros estados (perfil, suporte, etc)

if __name__ == '__main__':
    # Token do seu bot gerado no BotFather
    app = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot rodando...")
    app.run_polling()
    
