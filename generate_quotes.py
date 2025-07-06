import json
import random
import re
from faker import Faker
import base64
from datetime import datetime
import asyncio

fake = Faker("id_ID")

JUMLAH_DATA = 1010

BANK_LIST = [
    "Bank BCA", "Bank Mandiri", "Bank BRI",
    "Bank BNI", "Bank BTN", "Bank CIMB Niaga"
]

NOMINAL_OPTIONS = [
    50000, 100000, 200000, 500000,
    1000000, 2000000, 5000000
]

# Escape MarkdownV2 (kecuali titik)
def escape_md_except_dot(text: str) -> str:
    # Semua karakter MarkdownV2 harus di-escape kecuali titik (.)
    return re.sub(r'([_*\[\]()~`>#+=|{}!\\-])', r'\\\1', str(text))

# Enkripsi email base64
def encrypt_email_base64(email: str) -> str:
    return base64.b64encode(email.encode("utf-8")).decode("utf-8")

def generate_transaksi():
    raw_nama = fake.name()
    # Hapus '/' dan '\'
    clean_nama = raw_nama.replace('/', '').replace('\\', '')
    # Escape tapi jangan escape titik
    nama = escape_md_except_dot(clean_nama)

    email = encrypt_email_base64(fake.email())
    trx_id = f"TRX-{random.randint(10000000, 99999999)}"
    jumlah = f"Rp {random.choice(NOMINAL_OPTIONS):,}".replace(",", ".")
    bank = escape_md_except_dot(random.choice(BANK_LIST))

    waktu = datetime.now().strftime("%d %B %Y, %H:%M WIB")

    return (
        f"*📥 Pemberitahuan Transaksi Deposit Masuk*\n\n"
        f"✅ Transaksi deposit baru telah diterima.\n"
        f"🔒 _Data pengguna telah dienkripsi untuk menjaga keamanan._\n\n"
        f"*👤 Nama:* {nama}\n"
        f"*📧 Email (terenkripsi):* `{email}`\n"
        f"*🆔 ID Transaksi:* `{trx_id}`\n"
        f"*💰 Jumlah Deposit:* *{jumlah}*\n"
        f"*🕓 Tanggal & Waktu:* {waktu}\n"
        f"*🏦 Merchant:* {bank} - Virtual Account\n\n"
        f"🔐 _Seluruh data pengguna telah dienkripsi untuk memastikan keamanan dan kerahasiaan informasi._"
    )

async def generate_loop():
    while True:
        quotes = [generate_transaksi() for _ in range(JUMLAH_DATA)]
        with open("quotes.json", "w", encoding="utf-8") as f:
            json.dump(quotes, f, ensure_ascii=False, indent=2)
        print(f"✅ quotes.json berhasil dibuat ulang pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        await asyncio.sleep(420000)  # tunggu 1 jam

if __name__ == "__main__":
    asyncio.run(generate_loop())