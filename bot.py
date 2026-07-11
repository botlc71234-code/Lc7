import os
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from flask import Flask
from threading import Thread

# --- ID DO ADMINISTRADOR ---
ADMIN_ID = "8827427559"

# --- PERSISTÊNCIA DE DADOS ---
DB_FILE = "dados_bot.json"

def carregar_dados():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def salvar_dados():
    with open(DB_FILE, "w") as f:
        json.dump(users_db, f)

# --- BANCO DE DADOS ---
users_db = carregar_dados()

# --- VITRINE DE PRODUTOS ---
produtos = [
    {
        "id": 1,
        "bin": "516292",
        "nome": "Cartão Nubank Platinum - Mastercard",
        "preco": 2.00,
        "demonstracao": "✨ *Detalhes do cartão*\n💳 *Cartão:* 516292*********\n📆 *Validade:* 07/2033\n🔐 *Cod:* ***\n\n🏳️ *Bandeira:* mastercard\n💠 *Nível:* nubank platinum\n⚜️ *Tipo:* credit\n🏛 *Banco:* nu pagamentos sa\n🌍 *Pais:* brazil\n\n👤 *Nome:* vanessa g almeida\n🪪 *cpf:* 25845634873",
        "completo": "✅ *COMPRA APROVADA!*\n\n✨ *Dados do cartão*\n💳 *Cartão:* 516292000055267\n📆 *Validade:* 07/2033\n🔐 *Cod:* 363\n\n👤 *Nome:* vanessa g almeida\n🪪 *cpf:* 25845634873"
    },
    {
        "id": 2,
        "bin": "516292",
        "nome": "Cartão Nubank Platinum - Mastercard",
        "preco": 2.00,
        "demonstracao": "✨ *Detalhes do cartão*\n💳 *Cartão:* 516292*********\n📆 *Validade:* 07/2033\n🔐 *Cod:* ***\n\n🏳️ *Bandeira:* mastercard\n💠 *Nível:* nubank platinum\n⚜️ *Tipo:* credit\n🏛 *Banco:* nu pagamentos sa\n🌍 *Pais:* brazil\n\n👤 *Nome:* marcos g almeida\n🪪 *cpf:* 25845634873",
        "completo": "✅ *COMPRA APROVADA!*\n\n✨ *Dados do cartão*\n💳 *Cartão:* 516292000055267\n📆 *Validade:* 07/2043\n🔐 *Cod:* 500\n\n👤 *Nome:* marcos g almeida\n🪪 *cpf:* 25845634873"
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

# --- FUNÇÃO BUSCA BIN ---
async def buscar_bin(update, context):
    if len(context.args) != 1:
        await update.message.reply_text("⚠️ Use: /bin 550209")
        return
    bin_procurado = context.args[0]
    resultados = [p for p in produtos if p['bin'].startswith(bin_procurado)]
    if not resultados:
        await update.message.reply_text(f"❌ Nenhum produto encontrado para o BIN: `{bin_procurado}`", parse_mode='Markdown')
    else:
        msg = f"🔍 *Resultados para o BIN {bin_procurado}:*\n\n"
        for p in resultados:
            msg += f"• {p['nome']} - R$ {p['preco']:.2f}\n"
        await update.message.reply_text(msg, parse_mode='Markdown')

# --- FUNÇÃO ADMIN ---
async def admin_add_saldo(update, context):
    user_id = str(update.effective_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Acesso negado.")
        return
    if len(context.args) != 2:
        await update.message.reply_text("⚠️ Use: /addsaldo ID_USUARIO VALOR")
        return
    target_id = context.args[0]
    valor = float(context.args[1])
    if target_id not in users_db:
        users_db[target_id] = {"saldo": 0.00, "compras": []}
    users_db[target_id]["saldo"] += valor
    salvar_dados()
    await update.message.reply_text(f"✅ Saldo de R$ {valor:.2f} adicionado ao ID `{target_id}`.", parse_mode='Markdown')

# --- FUNÇÃO EXIBIR PRODUTO ---
async def exibir_produto(query, idx):
    if not produtos:
        await query.edit_message_text("❌ Não há mais produtos disponíveis no momento.")
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

# --- MENU E START ---
def get_menu_markup():
    keyboard = [
        [InlineKeyboardButton("💰 Adiciona Saldo", callback_data='saldo')],
        [InlineKeyboardButton("💳 CC FULL DADOS", callback_data='cc')],
        [InlineKeyboardButton("🔍 Busca bin", callback_data='bin')],
        [InlineKeyboardButton("« volta", callback_data='start')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update, context):
    user_id = str(update.effective_user.id)
    if user_id not in users_db:
        users_db[user_id] = {"saldo": 0.00, "compras": []}
        salvar_dados()
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
    user_id = str(update.effective_user.id)
    if user_id not in users_db:
        users_db[user_id] = {"saldo": 0.00, "compras": []}
    
    if query.data == 'menu':
        await query.edit_message_text("Escolha uma opção no menu abaixo:", reply_markup=get_menu_markup())
    elif query.data == 'cc':
        await exibir_produto(query, 0)
    elif query.data == 'bin':
        await query.edit_message_text("🔍 Use o comando no chat:\n/bin 550209")
    elif query.data.startswith('prod_'):
        _, acao, idx = query.data.split('_')
        idx = int(idx)
        if acao == 'prev':
            await exibir_produto(query, idx - 1)
        elif acao == 'next':
            await exibir_produto(query, idx + 1)
        elif acao == 'buy':
            produto = produtos[idx]
            if users_db[user_id]["saldo"] >= produto['preco']:
                users_db[user_id]["saldo"] -= produto['preco']
                users_db[user_id]["compras"].append(produto['completo'])
                salvar_dados()
                await context.bot.send_message(chat_id=update.effective_chat.id, text=produto['completo'], parse_mode='Markdown')
                produtos.pop(idx)
                if len(produtos) > 0:
                    await exibir_produto(query, 0)
                else:
                    await query.edit_message_text("❌ Nenhum produto disponível.")
            else:
                await query.answer("❌ Saldo insuficiente!", show_alert=True)
    elif query.data == 'perfil':
        saldo = users_db[user_id].get("saldo", 0.00)
        keyboard = [
            [InlineKeyboardButton("💳 Minhas CC", callback_data='minhas_cc')],
            [InlineKeyboardButton("« volta", callback_data='start')]
        ]
        texto_perfil = f"👤 **SEU PERFIL**\n\n🆔 ID: `{user_id}`\n💰 SALDO: R$ {saldo:.2f}"
        await query.edit_message_text(texto_perfil, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    elif query.data == 'minhas_cc':
        compras = users_db[user_id].get("compras", [])
        if not compras:
            await query.answer("Você não tem compras.", show_alert=True)
        else:
            for cc in compras:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=cc, parse_mode='Markdown')
    elif query.data == 'start':
        await start(update, context)
    elif query.data == 'regras':
        await query.edit_message_text("⚠️ Regras: Solicite troca em até 5 minutos com vídeo (GPAY).", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« volta", callback_data='start')]]))

if __name__ == '__main__':
    Thread(target=run_web).start()
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addsaldo", admin_add_saldo))
    app.add_handler(CommandHandler("bin", buscar_bin))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
                                         
