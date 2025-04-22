
# 🤖 BuyDetector™ by ReactLAB

A Telegram bot that monitors ETH transactions on a specific address and alerts your group with:

- 🪙 Live ETH amount & USD conversion
- 🔵 Visual bullet indicators (0.05 ETH = 1 bullet)
- 💼 Realtime wallet balance + USD value
- 📊 Etherscan link
- 🖼️ Optional GIF support
- 🛠️ Markdown formatting with aesthetic branding

---

### 🌐 Powered by [ReactLAB](https://pandabao.org/)
_Crafted for DeFi founders & stealth launches._

---

## 📦 How it works

- Scans a specified Ethereum wallet (like a presale contract).
- Detects new transactions using the [Etherscan API](https://etherscan.io/apis).
- Fetches ETH-USD conversion using [CoinGecko API](https://www.coingecko.com/en/api).
- Sends Telegram messages formatted with all key info + media.

---

## ⚙️ .env Configuration

Create a `.env` file in your root directory:

```env
TELEGRAM_TOKEN=your_bot_token
CHAT_ID=your_group_or_channel_id
ETHERSCAN_API_KEY=your_etherscan_key
GIF_URL=https://yourdomain.com/yourgif.gif  # optional
🚀 Deploy to Railway
You can deploy this bot instantly using Railway:

Fork this repo.

Connect your GitHub repo in Railway.

Set the environment variables (.env) in the Railway dashboard.

Deploy.

🧪 Sample Output
bash
Copy
Edit
🪙 New $GOV movement detected!

🔁 From: 0x...
📥 To: 0x...
💰 Amount: 0.1500 ETH (~$487.50)
🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵

📊 Total Balance: 15.2844 ETH (~$49,500.00)
🔗 View on Etherscan

⚱️ Powered by Chrysus  
🌐 https://chrysus.org  
🌐 https://pinksale.finance/...

───────────────  
🤖 𝓑𝓾𝔂𝓓𝓮𝓽𝓮𝓬𝓽𝓸𝓻™  
🔧 𝒃𝒚 [𝑹𝒆𝒂𝒄𝒕𝑳𝑨𝑩](https://pandabao.org/)  
───────────────
🛡️ License
MIT © ReactLAB
