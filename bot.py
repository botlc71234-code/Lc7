import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from flask import Flask
from threading import Thread

# --- CONFIGURAÇÃO DO FLASK (Para manter o bot ativo no Render) ---
app_web = Flask(__name__)
@app_web.route('/')
def home():
    return "Bot Lc7 online!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# --- COMANDO /START ---
async def start(update, context):
    texto = (
        "👋 SEJA BEM-VINDO A OROCHI_STORE AS MELHORES FULL DADOS ESTAO AQUI 🚀\n"
        "✅ MATERIAL 100% VIRGEM✅\n"
        "📊 MATERIAL PREMIUM DE ADMIN FULL DADOS COM GARANTIA DE CPF 100% BATENDO!\n"
        "🔍 PARA CONSULTAR CPF ANTES DA COMPRA, BASTAR TER 30$ DE SALDO DISPONIVEL NO BOT.\n\n"
        "📌 REGRAS GERAIS:\n"
        "📸 PARA SOLICITAR TROCA, E OBRIGATORIO:\n"
        "⏰ SOLICITAR DENTRO DO PRAZO DE 5 MINUTOS APOS A COMPRA.\n"
        "🧪 SO ACEITAMOS VIDEO DO TESTE NO (GPAY) NAO ACEITAMOS PRINT LEMBRANDO QUE TEM QUE ESTAR DENTRO DO PRAZO CITADO.\n"
        "📲 DUVIDAS OU PROBLEMAS? FALE COM NOSSO SUPORTE @SUPORTEOROCHICCS"
    )

    keyboard = [
        [InlineKeyboardButton("Menu", callback_data='menu'), InlineKeyboardButton("Seu Perfil", callback_data='perfil')],
        [InlineKeyboardButton("🛠️ SUPORTE", callback_data='suporte')],
        [InlineKeyboardButton("⚠️ REGRAS DE TROCA⚠️", callback_data='regras')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(texto, reply_markup=reply_markup)

# --- COMANDO /BIN ---
async def bin_command(update, context):
    await update.message.reply_text(
        "💳 **MENU DE BINS**\n\n"
        "Escolha uma opção abaixo para consultar ou ver listas:\n"
        "Exemplo: Consulte sua BIN disponível."
    )

# --- GERENCIADOR DE BOTÕES ---
async def button(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'menu':
        await query.edit_message_text("🛒 Menu de Compras: (Em breve)")
    elif query.data == 'perfil':
        await query.edit_message_text("👤 Perfil: Você está conectado.")
    elif query.data == 'suporte':
        await query.edit_message_text("🛠️ Suporte: Entre em contato com @SUPORTEOROCHICCS")
    elif query.data == 'regras':
        await query.edit_message_text("⚠️ Regras: Solicite troca em até 5 minutos com vídeo (GPAY).")

# --- INICIALIZAÇÃO ---
if __name__ == '__main__':
    # Inicia o servidor web em uma thread separada
    Thread(target=run_web).start()
    
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Adiciona os comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bin", bin_command))
    app.add_handler(CallbackQueryHandler(button))
    
    app.run_polling()
    
