import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from flask import Flask
from threading import Thread

# Configuração do Flask (Para o Render não desligar o bot)
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot Lc7 está online!"

def run_web():
    app_web.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# --- FUNÇÕES DOS COMANDOS ---
async def start(update, context):
    await update.message.reply_text("Olá! Sou o bot Lc7. Use /perfil, /comprar ou /suporte.")

async def perfil(update, context):
    await update.message.reply_text("👤 Perfil: Você está conectado ao bot do repositório Lc7.")

async def comprar(update, context):
    await update.message.reply_text("🛒 Menu de Compras: (Em breve integraremos com métodos de pagamento).")

async def suporte(update, context):
    await update.message.reply_text("🛠️ Suporte: Se tiver dúvidas, abra uma issue no nosso GitHub!")

# --- INICIALIZAÇÃO ---
if __name__ == '__main__':
    # Inicia o servidor Flask em uma thread separada
    Thread(target=run_web).start()

    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("perfil", perfil))
    app.add_handler(CommandHandler("comprar", comprar))
    app.add_handler(CommandHandler("suporte", suporte))
    
    app.run_polling()
    
