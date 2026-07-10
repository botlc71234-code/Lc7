import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
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

# --- GERENCIADOR DE MENSAGENS (BUSCA BIN) ---
async def buscar_bin(update, context):
    mensagem = update.message.text.split()
    if len(mensagem) > 1:
        bin_digitada = mensagem[1]
        # AQUI VOCÊ EDITA AS FRASES PARA CADA BIN
        if bin_digitada == "516262":
            resultado = (
                f"🔍 **RESULTADO DA BIN: {bin_digitada}**\n\n"
                "🏦 Banco: Nubank\n"
                "💠 Nível: Gold\n"
                "⚜ Tipo: Crédito\n"
                "✅ BIN Aprovada e testada!"
            )
        else:
            resultado = f"❌ BIN {bin_digitada} não encontrada ou inválida."
        
        await update.message.reply_text(resultado, parse_mode='Markdown')
    else:
        await update.message.reply_text("⚠️ Por favor, digite /bin seguido do número. Exemplo: /bin 516262")

# --- GERENCIADOR DE BOTÕES ---
async def button(update, context):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    if query.data == 'menu':
        texto_menu = "Escolha uma opção no menu abaixo:"
        await query.edit_message_text(texto_menu, reply_markup=get_menu_markup())

    elif query.data == 'bin':
        await query.edit_message_text("Digite /bin seguido dos 6 primeiros números do cartão.\nExemplo: /bin 516262")

    elif query.data == 'cc':
        texto_cc = (
            "💳 **LISTA DE CC FULL DADOS**\n\n"
            "✨ **Detalhes do cartão**\n"
            "💳 cartão: `55020962828282`\n"
            "✅ INFORMAÇÕES VIRGENS DIRETO DO ADMIN (SNIFFER)\n\n"
            "Selecione uma categoria para visualizar os preços."
        )
        keyboard = [[InlineKeyboardButton("« volta", callback_data='menu')]]
        await query.edit_message_text(texto_cc, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'perfil':
        saldo = users_db.get(user_id, {}).get("saldo", 0.00)
        texto_perfil = (f"👤 **SEU PERFIL**\n\n💰 SALDO: R$ {saldo:.2f}")
        keyboard = [[InlineKeyboardButton("« volta", callback_data='start')]]
        await query.edit_message_text(texto_perfil, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'start':
        await start(update, context)
    
    elif query.data == 'regras':
        keyboard = [[InlineKeyboardButton("« volta", callback_data='start')]]
        await query.edit_message_text("⚠️ Regras: Solicite troca em até 5 minutos com vídeo.", reply_markup=InlineKeyboardMarkup(keyboard))

# --- INICIALIZAÇÃO ---
if __name__ == '__main__':
    Thread(target=run_web).start()
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bin", buscar_bin)) # Adicionado o comando /bin
    app.add_handler(CallbackQueryHandler(button))
    
    app.run_polling()
    
