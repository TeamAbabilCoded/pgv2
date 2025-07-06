import json
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import BotBlocked, ChatNotFound
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import time
import pytz

# === Konfigurasi ===
API_TOKEN = '8118828836:AAFTy8VS4LTgIr3amxNS4PV9fHjR7H7aAIw'
GROUP_CHAT_ID = -1001521005536
ADMIN_USERNAME = 'BrimboStockOfficial'
# ====================

bot = Bot(token=API_TOKEN, parse_mode="Markdown")  # Gunakan Markdown, bukan MarkdownV2
dp = Dispatcher(bot)

def get_random_quote():
    with open('quotes.json', 'r', encoding='utf-8') as file:
        quotes = json.load(file)
    quote_template = random.choice(quotes)

    # Format waktu untuk menggantikan {datetime}
    now = datetime.now(pytz.timezone("Asia/Jakarta"))
    formatted_time = now.strftime("%d %B %Y, %H:%M WIB")

    # Ambil ID Transaksi dari isi teks
    trx_id = "UNKNOWN"
    for word in quote_template.split():
        if word.startswith("TRX-"):
            trx_id = word.strip("`")  # hapus backtick

    # Ganti {datetime} dengan waktu asli
    final_message = quote_template.replace("{datetime}", formatted_time)
    return final_message, trx_id

async def send_random_message():
    while True:
        try:
            message_text, trx_id = get_random_quote()

            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                InlineKeyboardButton("🔍 Lihat Detail Transaksi", url=f"https://contoh-transaksi.com/{trx_id}"),
                InlineKeyboardButton("📞 Hubungi Admin", url=f"https://t.me/{ADMIN_USERNAME}")
            )

            await bot.send_message(chat_id=GROUP_CHAT_ID, text=message_text, reply_markup=keyboard)
            print(f"✅ Pesan terkirim:\n{message_text}")
        except (BotBlocked, ChatNotFound):
            print("⚠️ Gagal mengirim pesan. Pastikan bot sudah jadi admin di grup.")
        await asyncio.sleep(890)    # jeda 3 detik (ubah jika perlu)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(send_random_message())
    loop.run_forever()