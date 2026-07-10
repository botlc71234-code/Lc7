import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from flask import Flask
from threading import Thread

# --- BANCO DE DADOS SIMPLES (Memória) ---
users_db = {}

# --- VITRINE DE PRODUTOS ---
produtos = [
    {
        "id": 1,
        "bin": "516292",
        "nome": "Cartão Nubank Platinum - Mastercard",
        "preco": 2.00,
        "demonstracao": "✨ *Detalhes do cartão*\n💳 *Cartão:* 516292*********\n📆 *Validade:* 07/2033\n🔐 *Cod:* ***\n\n🏳️ *Bandeira:* mastercard\n💠 *Nível:* nubank platinum\n⚜️ *Tipo:* credit\n🏛 *Banco:* nu pagamentos sa\n🌍 *Pais:* brazil\n\n👤 *Nome:* vanessa g almeida\n🪪 *cpf:* 25845634873"
    },
    {
        "id": 2,
        "bin": "516292",
        "nome": "Cartão Nubank Platinum - Mastercard",
        "preco": 2.00,
        "demonstracao": "✨ *Detalhes do cartão*\n💳 *Cartão:* 516292*********\n📆 *Validade:* 07/2033\n🔐 *Cod:* ***\n\n🏳️ *Bandeira:* mastercard\n💠 *Nível:* nubank platinum\n⚜️ *Tipo:* credit\n🏛 *Banco:* nu pagamentos sa\n🌍 *Pais:* brazil\n\n👤 *Nome:* marcos g almeida\n🪪 *cpf:* 25845634873"
    }
]

# --- CONFIGURAÇÃO DO FLASK ---
app_web = Flask(__name__)
@app_web.route('/')
def home():
    return "Bot Lc7 online!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# --- FUNÇÃO PARA EXIBIR PRODUTO ---
async def exibir_produto(query, idx):
    idx = max(0, min(idx, len(produtos) - 1))
    p = produtos[idx]
    
    texto = f"📦 *Item {idx + 1} de {len(produtos)}*\n\n{p['demonstracao']}"
    
    keyboard = [
        [
            InlineKeyboardButton("« Anterior", callback_data=f'prod_prev_{idx}'),
            InlineKeyboardButton("Próximo »", callback_data=f'prod_next_{idx}')
        ],
        [InlineKeyboardButton(f"💰 COMPRAR - R$ {p['preco']:.2f}", callback_data=f'prod_buy_{idx}')],
        [InlineKeyboardButton("« volta ao menu", callback_data='menu')]
    ]
    
    await query.edit_message_text(texto, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# --- MENU PRINCIPAL ---
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
    
    if query.data == 'menu':
        await query.edit_message_text("Escolha uma opção no menu abaixo:", reply_markup=get_menu_markup())

    elif query.data == 'cc':
        await exibir_produto(query, 0)

    elif query.data.startswith('prod_'):
        _, acao, idx = query.data.split('_')
        idx = int(idx)
        if acao == 'prev':
            await exibir_produto(query, idx - 1)
        elif acao == 'next':
            await exibir_produto(query, idx + 1)
        elif acao == 'buy':
            await query.answer("Processando compra...", show_alert=True)
            await query.message.reply_text(f"✅ Compra do Item {idx + 1} iniciada!")

    elif query.data == 'perfil':
        user_id = update.effective_user.id
        saldo = users_db.get(user_id, {}).get("saldo", 0.00)
        texto_perfil = f"👤 **SEU PERFIL**\n\n🆔 ID: `{user_id}`\n💰 SALDO: R$ {saldo:.2f}\n\nUse o menu principal para adicionar saldo."
        await query.edit_message_text(texto_perfil, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« volta", callback_data='start')]]), parse_mode='Markdown')

    elif query.data == 'start':
        await start(update, context)
    
    elif query.data == 'regras':
        await query.edit_message_text("⚠️ Regras: Solicite troca em até 5 minutos com vídeo (GPAY).", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« volta", callback_data='start')]]))

if __name__ == '__main__':
    Thread(target=run_web).start()
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
    
