import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from flask import Flask
from threading import Thread

# --- ID DO ADMINISTRADOR ---
ADMIN_ID = "8827427559"

# --- BANCO DE DADOS ---
# Cada usuário agora tem 'saldo' e uma lista 'compras'
users_db = {}

# --- VITRINE DE PRODUTOS ---
produtos = [
    {
        "id": 1,
        "nome": "Cartão Nubank Platinum - Mastercard",
        "preco": 2.00,
        "demonstracao": "✨ *Detalhes do cartão*\n💳 *Cartão:* 516292*********\n📆 *Validade:* 07/2033\n🔐 *Cod:* ***\n\n🏳️ *Bandeira:* mastercard\n💠 *Nível:* nubank platinum\n⚜️ *Tipo:* credit\n🏛 *Banco:* nu pagamentos sa\n🌍 *Pais:* brazil\n\n👤 *Nome:* vanessa g almeida\n🪪 *cpf:* 25845634873",
        "completo": "✅ *COMPRA APROVADA!*\n\n✨ *Dados do cartão*\n💳 *Cartão:* 516292000055267\n📆 *Validade:* 07/2033\n🔐 *Cod:* 363\n\n👤 *Nome:* vanessa g almeida\n🪪 *cpf:* 25845634873"
    },
    {
        "id": 2,
        "nome": "Cartão Nubank Platinum - Mastercard",
        "preco": 2.00,
        "demonstracao": "✨ *Detalhes do cartão*\n💳 *Cartão:* 516292*********\n📆 *Validade:* 07/2033\n🔐 *Cod:* ***\n\n🏳️ *Bandeira:* mastercard\n💠 *Nível:* nubank platinum\n⚜️ *Tipo:* credit\n🏛 *Banco:* nu pagamentos sa\n🌍 *Pais:* brazil\n\n👤 *Nome:* marcos g almeida\n🪪 *cpf:* 25845634873",
        "completo": "✅ *COMPRA APROVADA!*\n\n✨ *Dados do cartão*\n💳 *Cartão:* 516292000055267\n📆 *Validade:* 07/2043\n🔐 *Cod:* 500\n\n👤 *Nome:* marcos g almeida\n🪪 *cpf:* 25845634873"
    }
]

# --- CONFIGURAÇÃO WEB ---
app_web = Flask(__name__)
@app_web.route('/')
def home():
    return "Bot Lc7 online!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# --- FUNÇÕES ADMIN ---
async def admin_add_saldo(update, context):
    if str(update.effective_user.id) != ADMIN_ID: return
    if len(context.args) != 2: return
    target_id = int(context.args[0])
    valor = float(context.args[1])
    if target_id not in users_db: users_db[target_id] = {"saldo": 0.00, "compras": []}
    users_db[target_id]["saldo"] += valor
    await update.message.reply_text(f"✅ Saldo de R$ {valor:.2f} adicionado ao ID `{target_id}`.", parse_mode='Markdown')

# --- FUNÇÕES VITRINE ---
async def exibir_produto(query, idx):
    if not produtos:
        await query.edit_message_text("❌ Nenhum produto disponível.")
        return
    idx = max(0, min(idx, len(produtos) - 1))
    p = produtos[idx]
    texto = f"📦 *Item {idx + 1} de {len(produtos)}*\n\n{p['demonstracao']}\n\n⠀"
    keyboard = [
        [InlineKeyboardButton("« Anterior", callback_data=f'prod_prev_{idx}'), InlineKeyboardButton("Próximo »", callback_data=f'prod_next_{idx}')],
        [InlineKeyboardButton(f"💰 COMPRAR - R$ {p['preco']:.2f}", callback_data=f'prod_buy_{idx}')],
        [InlineKeyboardButton("« volta ao menu", callback_data='menu')]
    ]
    await query.edit_message_text(texto, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def start(update, context):
    user_id = update.effective_user.id
    if user_id not in users_db: users_db[user_id] = {"saldo": 0.00, "compras": []}
    texto = "👋 SEJA BEM-VINDO A OROCHI_STORE!"
    keyboard = [[InlineKeyboardButton("Menu", callback_data='menu'), InlineKeyboardButton("Seu Perfil", callback_data='perfil')]]
    if update.message: await update.message.reply_text(texto, reply_markup=InlineKeyboardMarkup(keyboard))
    else: await update.callback_query.edit_message_text(texto, reply_markup=InlineKeyboardMarkup(keyboard))

# --- BOTÕES ---
async def button(update, context):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    if user_id not in users_db: users_db[user_id] = {"saldo": 0.00, "compras": []}
    
    if query.data == 'menu':
        await query.edit_message_text("Menu:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💰 Saldo", callback_data='saldo')], [InlineKeyboardButton("💳 CC FULL DADOS", callback_data='cc')], [InlineKeyboardButton("« volta", callback_data='start')]]))
    elif query.data == 'cc': await exibir_produto(query, 0)
    elif query.data.startswith('prod_'):
        _, acao, idx = query.data.split('_')
        idx = int(idx)
        if acao == 'prev': await exibir_produto(query, idx - 1)
        elif acao == 'next': await exibir_produto(query, idx + 1)
        elif acao == 'buy':
            produto = produtos[idx]
            if users_db[user_id]["saldo"] >= produto['preco']:
                users_db[user_id]["saldo"] -= produto['preco']
                users_db[user_id]["compras"].append(produto['completo'])
                await query.answer("Compra realizada!", show_alert=True)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=produto['completo'], parse_mode='Markdown')
                produtos.pop(idx)
                if len(produtos) > 0: await exibir_produto(query, 0)
                else: await query.edit_message_text("❌ Nenhum produto disponível.")
            else: await query.answer("❌ Saldo insuficiente!", show_alert=True)
    elif query.data == 'perfil':
        saldo = users_db[user_id].get("saldo", 0.00)
        keyboard = [[InlineKeyboardButton("💳 Minhas CC", callback_data='minhas_cc')], [InlineKeyboardButton("« volta", callback_data='start')]]
        await query.edit_message_text(f"💰 SALDO: R$ {saldo:.2f}", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == 'minhas_cc':
        compras = users_db[user_id].get("compras", [])
        if not compras: await query.answer("Você não comprou nada.", show_alert=True)
        else:
            for cc in compras: await context.bot.send_message(chat_id=update.effective_chat.id, text=cc, parse_mode='Markdown')
    elif query.data == 'start': await start(update, context)

if __name__ == '__main__':
    Thread(target=run_web).start()
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addsaldo", admin_add_saldo))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
    
