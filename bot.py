import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Configuração básica de log para vermos se o bot está funcionando
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- FUNÇÕES DOS COMANDOS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Sou seu bot. Use os comandos:\n/perfil - Ver dados\n/comprar - Ver produtos\n/suporte - Ajuda")

async def perfil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Aqui você pode expandir para buscar dados reais
    await update.message.reply_text("👤 Perfil: Você está conectado ao bot do repositório Lc7.")

async def comprar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛒 Menu de Compras: (Em breve integraremos com métodos de pagamento).")

async def suporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛠️ Suporte: Se tiver dúvidas, abra uma issue no nosso GitHub!")

# --- INICIALIZAÇÃO ---

if __name__ == '__main__':
    # O token será pego de forma segura nas configurações do Render
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    if not TOKEN:
        print("Erro: TELEGRAM_TOKEN não configurado!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        
        # Adiciona os comandos
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("perfil", perfil))
        app.add_handler(CommandHandler("comprar", comprar))
        app.add_handler(CommandHandler("suporte", suporte))
        
        print("Bot iniciado...")
        app.run_polling()
      
