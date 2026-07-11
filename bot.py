import os
import sqlite3
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from flask import Flask
from threading import Thread

# --- CONFIGURAÇÃO ---
ADMIN_ID = "8827427559"
DB_NAME = "dados_bot.db"

# --- BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    # Tabela de usuários com histórico de compras em JSON
    conn.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, saldo REAL, compras TEXT)")
    # Tabela de produtos
    conn.execute("""CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, bin TEXT, nome TEXT, preco REAL, 
        demonstracao TEXT, completo TEXT)""")
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

# --- FUNÇÕES DE DADOS ---
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT saldo, compras FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"saldo": row[0], "compras": json.loads(row[1])}
    return {"saldo": 0.00, "compras": []}

def save_user(user_id, saldo, compras):
    conn = get_db_connection()
    conn.execute("REPLACE INTO users (user_id, saldo, compras) VALUES (?, ?, ?)", 
                 (user_id, saldo, json.dumps(compras)))
    conn.commit()
    conn.close()

# --- FLASK ---
app_web = Flask(__name__)
@app_web.route('/')
def home(): return "Bot Lc7 online!"
def run_web(): app_web.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# --- FUNÇÕES ---
async def start(update, context):
    user_id = str(update.effective_user.id)
    # Cria o usuário se não existir
    data = get_user(user_id)
    save_user(user_id, data["saldo"], data["compras"])
    
    texto = "👋 SEJA BEM-VINDO A OROCHI_STORE!"
    keyboard = [
        [InlineKeyboardButton("Menu", callback_data='menu'), InlineKeyboardButton("Seu Perfil", callback_data='perfil')],
        [InlineKeyboardButton("🛠️ SUPORTE", url="https://wa.me/5511999999999")]
    ]
    if update.message: await update.message.reply_text(texto, reply_markup=InlineKeyboardMarkup(keyboard))
    else: await update.callback_query.edit_message_text(texto, reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update, context):
    query = update.callback_query
    await query.answer()
    user_id = str(update.effective_user.id)
    data = get_user(user_id)

    if query.data == 'menu':
        keyboard = [
            [InlineKeyboardButton("💰 Adicionar Saldo", callback_data='saldo')],
            [InlineKeyboardButton("💳 CC FULL DADOS", callback_data='cc')],
            [InlineKeyboardButton("🔍 Busca bin", callback_data='bin')],
            [InlineKeyboardButton("« volta", callback_data='start')]
        ]
        await query.edit_message_text("Escolha uma opção:", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif query.data == 'cc':
        conn = get_db_connection()
        prod = conn.execute("SELECT * FROM produtos LIMIT 1").fetchone()
        conn.close()
        if prod:
            await query.edit_message_text(f"📦 Produto: {prod[2]}\nPreço: R$ {prod[3]}", 
                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💰 Comprar", callback_data=f'buy_{prod[0]}')]]))
        else:
            await query.edit_message_text("❌ Nenhum produto.")

    elif query.data.startswith('buy_'):
        pid = query.data.split('_')[1]
        conn = get_db_connection()
        prod = conn.execute("SELECT * FROM produtos WHERE id = ?", (pid,)).fetchone()
        if data["saldo"] >= prod[3]:
            data["saldo"] -= prod[3]
            data["compras"].append(prod[5])
            save_user(user_id, data["saldo"], data["compras"])
            conn.execute("DELETE FROM produtos WHERE id = ?", (pid,))
            conn.commit()
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"✅ APROVADO!\n{prod[5]}")
        else:
            await query.answer("❌ Saldo insuficiente!", show_alert=True)
        conn.close()

    elif query.data == 'perfil':
        await query.edit_message_text(f"💰 SALDO: R$ {data['saldo']:.2f}")

if __name__ == '__main__':
    init_db()
    Thread(target=run_web).start()
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
                                  
