import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from flask import Flask
from threading import Thread

# Configuração básica de log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Servidor Flask para manter o Render ativo
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot Lc7 está online!"

def run_web():
    # O Render define a porta automaticamente através da variável de ambiente PORT
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

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

    # O token é pego das variáveis de ambiente do Render
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    if not TOKEN:
        print("Erro: TELEGRAM_TOKEN não configurado no Render!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        
        # Adiciona os comandos
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("perfil", perfil))
        app.add_handler(CommandHandler("comprar", comprar))
        app.add_handler(CommandHandler("suporte", suporte))
        
        print("Bot iniciado com sucesso...")
        app.run_polling()
        
