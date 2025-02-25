import os
import aiohttp
import asyncio
from telegram import Bot

# Configurări - Citire variabile de mediu
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BSCSCAN_API_KEY = os.getenv("BSCSCAN_API_KEY")
CONTRACT_ADDRESS = "0x8f9eCCd7047855e82341c56cB60aa10EEffF3084"
API_URL = "https://api.bscscan.com/api"
IMAGE_URL = "https://pandabao.org/wp-content/uploads/2024/12/Telegram.jpg"

# Verificare dacă variabilele sunt setate corect
if not TELEGRAM_TOKEN:
    raise ValueError("⚠️ TELEGRAM_TOKEN lipsește! Verifică variabilele de mediu.")
if not CHAT_ID:
    raise ValueError("⚠️ CHAT_ID lipsește! Verifică variabilele de mediu.")
if not BSCSCAN_API_KEY:
    raise ValueError("⚠️ BSCSCAN_API_KEY lipsește! Verifică variabilele de mediu.")

# Inițializare bot Telegram
bot = Bot(token=TELEGRAM_TOKEN)

# Funcție pentru verificarea tranzacțiilor
async def check_transactions():
    last_tx = ""  # Salvează ultima tranzacție verificată
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{API_URL}?module=account&action=txlist&address={CONTRACT_ADDRESS}&sort=desc&apikey={BSCSCAN_API_KEY}") as response:
                    data = await response.json()

            if data.get("status") == "1" and "result" in data:
                latest_tx = data["result"][0]
                if latest_tx["hash"] != last_tx:
                    last_tx = latest_tx["hash"]  # Actualizare ultima tranzacție
                    amount = int(latest_tx["value"]) / 10**18

                    # Construire mesaj
                    message = (
                        "🐼🐼🐼🐼🐼\n"
                        "✨ **New Pandorian Join The Army** ✨\n\n"
                        f"💰 Amount: {amount} BNB\n"
                        f"🔗 [Check the transaction on BSCscan 🧐](https://bscscan.com/tx/{last_tx})"
                    )

                    # Trimitere mesaj și imagine
                    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
                    await bot.send_photo(chat_id=CHAT_ID, photo=IMAGE_URL)

        except Exception as e:
            print(f"⚠️ Eroare: {e}")
        
        await asyncio.sleep(30)  # Verificare la fiecare 30 de secunde

# Executare cod într-un loop async
if __name__ == "__main__":
    asyncio.run(check_transactions())
