import os
import aiohttp
import asyncio
from telegram import Bot
from telegram.ext import Updater, CommandHandler

# Configurări - Citire variabile de mediu
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BSCSCAN_API_KEY = os.getenv("BSCSCAN_API_KEY")
CONTRACT_ADDRESS = "0x8f9eCCd7047855e82341c56cB60aa10EEffF3084"
API_URL = "https://api.bscscan.com/api"

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
            # Cerere către BscScan API folosind aiohttp pentru a face cererea asincron
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{API_URL}?module=account&action=txlist&address={CONTRACT_ADDRESS}&sort=desc&apikey={BSCSCAN_API_KEY}") as response:
                    data = await response.json()

            # Verificare dacă răspunsul API este valid
            if data.get("status") == "1" and "result" in data:
                latest_tx = data["result"][0]
                if latest_tx["hash"] != last_tx:
                    last_tx = latest_tx["hash"]  # Actualizare ultima tranzacție
                    amount = int(latest_tx["value"]) / 10**18  # Conversie la unități de tokenuri
                    sender = latest_tx["from"]
                    
                    # Construire mesaj
                    message = (
                        f"🦑 Panda Bao Token Purchase! 🐼\n\n"
                        f"💥 Amount: {amount:.4f} BAO\n"
                        f"📅 Date: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(latest_tx['timeStamp'])))}\n"
                        f"🎯 BAO Bought: {amount:.2f}\n"
                        f"💰 Total Value: ${amount * 0.0001:.2f}\n"  # Calcularea valorii totale
                        f"📈 BAO Price: $0.0001\n"
                        f"🔗 [Check the transaction on BSCscan 🧐](https://bscscan.com/tx/{last_tx})"
                    )

                    # Trimitere mesaj pe Telegram
                    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
        except Exception as e:
            print(f"⚠️ Eroare: {e}")
        
        await asyncio.sleep(30)  # Verificare la fiecare 30 de secunde

# Executare cod într-un loop async
if __name__ == "__main__":
    asyncio.run(check_transactions())
