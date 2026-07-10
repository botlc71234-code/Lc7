import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from flask import Flask
from threading import Thread

# --- LISTA DE PRODUTOS ---
produtos = {
    'cc_1': {
        'nome': "Nubank Platinum",
        'preco': 28.00,
        'previa': "💳 Cartão: 516292******4434\n🔒 Cvv: ***\n💰 Preço: R$ 28.00",
        'completo': "✨ Detalhes (LIBERADO)\n💳 Cartão: 5162921641114434\n🔒 Cvv: 363"
    },
    'cc_2': {
        'nome': "Inter Gold",
        'preco': 40.00,
        'previa': "💳 Cartão: 523155******1234\n🔒 Cvv: ***\n💰 Preço: R$ 40.00",
        'completo': "✨ Detalhes (LIBERADO)\n💳 Cartão: 5231551234567890\n🔒 Cvv: 999"
    },
    'cc_3': {
        'nome': "Itaú Platinum",
        'preco': 35.00,
        'previa': "💳 Cartão: 401178******5678\n🔒 Cvv: ***\n💰 Preço: R$ 35.00",
        'completo': "✨ Detalhes (LIBERADO)\n💳 Cartão: 4011789999995678\n🔒 Cvv: 123"
    }
}

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
        # Criando botões para cada produto da lista
        keyboard = []
        for key, p in produtos.items():
            keyboard.append([InlineKeyboardButton(f"{p['nome']} - R${p['preco']:.2f}", callback_data=f'view_{key}')])
        keyboard.append([InlineKeyboardButton("« volta", callback_data='menu')])
        await query.edit_message_text("💳 Escolha um cartão para ver detalhes:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith('view_'):
        # Mostrando o produto selecionado
        cc_id = query.data.split('_')[1]
        p = produtos[cc_id]
        texto_cc = f"{p['previa']}\n\n{p['completo']}"
        keyboard = [[InlineKeyboardButton("« voltar aos cartões", callback_data='cc')]]
        await query.edit_message_text(texto_cc, reply_markup=InlineKeyboardMarkup(keyboard))

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
        
