import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from flask import Flask
from threading import Thread

# --- CONFIGURAÇÃO DO FLASK ---
app_web = Flask(__name__)
@app_web.route('/')
def home():
    return "Bot Lc7 online!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# --- MENU COM OS 3 BOTÕES ---
def get_menu_markup():
    keyboard = [
        [InlineKeyboardButton("💰 Adiciona Saldo", callback_data='saldo')],
        [InlineKeyboardButton("💳 CC FULL DADOS", callback_data='cc')],
        [InlineKeyboardButton("🔍 Busca bin", callback_data='bin')],
        [InlineKeyboardButton("« volta", callback_data='start')]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- COMANDO /START ---
async def start(update, context):
    texto = (
        "👋 SEJA BEM-VINDO A OROCHI_STORE AS MELHORES FULL DADOS ESTAO AQUI 🚀\n"
        "✅ MATERIAL 100% VIRGEM✅\n"
        "📊 MATERIAL PREMIUM DE ADMIN FULL DADOS COM GARANTIA DE CPF 100% BATENDO!\n"
        "🔍 PARA CONSULTAR CPF ANTES DA COMPRA, BASTAR TER 30$ DE SALDO DISPONIVEL NO BOT."
    )
    
    keyboard = [
        [InlineKeyboardButton("Menu", callback_data='menu'), InlineKeyboardButton("Seu Perfil", callback_data='perfil')],
        [InlineKeyboardButton("🛠️ SUPORTE", url="https://wa.me/5511999999999")], 
        [InlineKeyboardButton("⚠️ REGRAS DE TROCA⚠️", callback_data='regras')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(texto, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(texto, reply_markup=reply_markup)

# --- GERENCIADOR DE BOTÕES ---
async def button(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'menu':
        texto_menu = (
            "⚠️ REGRAS DE TROCA⚠️\n"
            "🗃️ PARA SOLICITAR TROCA, É OBRIGATÓRIO:\n"
            "✅ SOLICITAR DENTRO DO PRAZO DE 5 MINUTOS APÓS A COMPRA.\n"
            "🧪 TESTES DEVEM SER FEITOS EXCLUSIVAMENTE NO GPAY.\n"
            "🔗 LINK DA GPAY: https://payments.google.com/gp/w/u/0/home/paymentmethods\n"
            "⏱️ CCS FORA DO PRAZO NÃO TERÃO DIREITO À TROCA."
        )
        await query.edit_message_text(texto_menu, reply_markup=get_menu_markup())

    elif query.data == 'start':
        await start(update, context)
    
    elif query.data == 'perfil':
        await query.edit_message_text("👤 Perfil: Você está conectado.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« volta", callback_data='start')]]))
    
    elif query.data == 'regras':
        await query.edit_message_text("⚠️ Regras: Solicite troca em até 5 minutos com vídeo (GPAY).", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« volta", callback_data='start')]]))

# --- INICIALIZAÇÃO ---
if __name__ == '__main__':
    Thread(target=run_web).start()
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    
    app.run_polling()
    
