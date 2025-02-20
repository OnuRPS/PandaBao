import os
import requests
import time
from telegram import Bot

# Configurări
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CONTRACT_ADDRESS = "0x8f9eCCd7047855e82341c56cB60aa10EEffF3084"
API_URL = "https://api.bscscan.com/api"
API_KEY = os.getenv("BSCSCAN_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)

# Funcție pentru verificarea tranzacțiilor
def check_transactions():
    last_tx = ""
    while True:
        try:
            response = requests.get(f"{API_URL}?module=account&action=txlist&address={CONTRACT_ADDRESS}&sort=desc&apikey={API_KEY}")
            data = response.json()
            if data["status"] == "1":
                latest_tx = data["result"][0]
                if latest_tx["hash"] != last_tx:
                    last_tx = latest_tx["hash"]
                    amount = int(latest_tx["value"]) / 10**18
                    sender = latest_tx["from"]
                    message = f"🔔 **Nouă tranzacție!**\n\n📤 De la: `{sender}`\n💰 Suma: {amount} BNB\n🔗 [Vezi pe BscScan](https://bscscan.com/tx/{last_tx})"
                    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
        except Exception as e:
            print(f"Eroare: {e}")
        time.sleep(30)  # Verificare la fiecare 30 de secunde

if __name__ == "__main__":
    check_transactions()
