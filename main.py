import os
import requests
import time
from telegram import Bot

# Configurări - Citire variabile de mediu
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BSCSCAN_API_KEY = os.getenv("BSCSCAN_API_KEY")
CONTRACT_ADDRESS = "0x8f9eCCd7047855e82341c56cB60aa10EEffF3084"
API_URL = "https://api.bscscan.com/api"

# Verificare dacă variabilele sunt setate corect
if not TELEGRAM_TOKEN:
    raise ValueError("⚠️ TELEGRAM_TOKEN lipsește! Verifică variabilele de mediu din Railway.")
if not CHAT_ID:
    raise ValueError("⚠️ CHAT_ID lipsește! Verifică variabilele de mediu din Railway.")
if not BSCSCAN_API_KEY:
    raise ValueError("⚠️ BSCSCAN_API_KEY lipsește! Verifică variabilele de mediu din Railway.")

# Inițializare bot Telegram
bot = Bot(token=TELEGRAM_TOKEN)

# Funcție pentru verificarea tranzacțiilor
def check_transactions():
    last_tx = ""  # Salvează ultima tranzacție verificată
    while True:
        try:
            # Cerere către BscScan API
            response = requests.get(f"{API_URL}?module=account&action=txlist&address={CONTRACT_ADDRESS}&sort=desc&apikey={BSCSCAN_API_KEY}")
            data = response.json()

            # Verificare dacă răspunsul API este valid
            if data.get("status") == "1" and "result" in data:
                latest_tx = data["result"][0]
                if latest_tx["hash"] != last_tx:
                    last_tx = latest_tx["hash"]  # Actualizare ultima tranzacție
                    amount = int(latest_tx["value"]) / 10**18
                    sender = latest_tx["from"]
                    
                    # Construire mesaj
                    message = (
                        f"🔔 **Nouă tranzacție!**\n\n"
                        f"📤 De la: `{sender}`\n"
                        f"💰 Suma: {amount} BNB\n"
                        f"🔗 [Vezi pe BscScan](https://bscscan.com/tx/{last_tx})"
                    )

                    # Trimitere mesaj pe Telegram
                    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
        except Exception as e:
            print(f"⚠️ Eroare: {e}")
        
        time.sleep(30)  # Verificare la fiecare 30 de secunde

# Executare cod
if __name__ == "__main__":
    check_transactions()
