import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from flask import Flask
from threading import Thread

# --- BANCO DE DADOS SIMPLES (Memória) ---
users_db = {}

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
    user_id = update.effective_user.id
    if user_id not in users_db:
        users_db[user_id] = {"saldo": 0.00}

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
    user_id = update.effective_user.id

    if query.data == 'menu':
        texto_menu = "Escolha uma opção no menu abaixo:"
        await query.edit_message_text(texto_menu, reply_markup=get_menu_markup())

    elif query.data == 'perfil':
        saldo = users_db.get(user_id, {}).get("saldo", 0.00)
        texto_perfil = (
            f"👤 **SEU PERFIL**\n\n"
            f"🆔 ID: `{user_id}`\n"
            f"💰 SALDO: R$ {saldo:.2f}\n\n"
            "Use o menu principal para adicionar saldo."
        )
        keyboard = [[InlineKeyboardButton("« volta", callback_data='start')]]
        await query.edit_message_text(texto_perfil, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'cc':
        texto_cc = (
            "🔍 *Mostrando 1 de 10*\n\n"
            "✨ *Detalhes do cartão*\n"
            "💳 *Cartão:* `5162921641114434`\n"
            "📅 *Validade:* 07/2033\n"
            "🔒 *Cvv:* 363\n\n"
            "🏳️ *Bandeira:* mastercard\n"
            "💎 *Nível:* nubank platinum\n"
            "⚜️ *Tipo:* credit\n"
            "🏛️ *Banco:* nu pagamentos sa\n"
            "🌎 *Pais:* brazil\n\n"
            "👤 *Nome:*\nvanessa g almeida\n"
            "🪪 *cpf:*\n25845634873\n\n"
            "💸 *Valor:* R$ 28.00\n"
            "📅 *Comprada em* 04/07/2026 ás 17:42:11"
        )
        keyboard = [[InlineKeyboardButton("« volta", callback_data='menu')]]
        await query.edit_message_text(texto_cc, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'start':
        await start(update, context)
    
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
    
