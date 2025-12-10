# Prakash Perplexity Bot

A Telegram bot that monitors cryptocurrency and stock market trends using Finnhub API and analyzes them with Perplexity AI to send intelligent trading alerts.

## Overview

This bot continuously monitors a watchlist of symbols (cryptocurrencies and stocks), detects significant price movements, and uses Perplexity AI to analyze and generate smart alerts that are sent directly to your Telegram.

## Features

- Real-time market monitoring via Finnhub API
- AI-powered trend analysis using Perplexity
- Automatic Telegram notifications for significant market movements
- Configurable watchlist and alert thresholds
- Support for both cryptocurrency and stock symbols

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   PPLX_API_KEY=your_perplexity_api_key
   FINNHUB_API_KEY=your_finnhub_api_key
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

## Configuration

Edit the `WATCHLIST`, `POLL_INTERVAL`, and `MIN_ABS_PCT_MOVE` variables in `main.py` to customize the bot behavior.

## License

This is an open source project. Feel free to use, modify, and distribute as needed.

## Support

If you find this project useful and would like to support its development, donations are welcome! You can contribute using any of the following wallet addresses:

### Cryptocurrency Donations

**Bitcoin (BTC):**
```
bc1qr9ahayl0wjmzakepaswdz0j934t5r2gz6avzva
```

**Ethereum (ETH):**
```
0xA4b5109E07203F128c70cD29A75f5BEC912411b9
```

**Binance Smart Chain (BSC):**
```
0xa4b5109e07203f128c70cd29a75f5bec912411b9
```

**Polygon (MATIC):**
```
0xa4b5109e07203f128c70cd29a75f5bec912411b9
```

**Solana (SOL):**
```
5dAgHxC4JACeaRW6Vftz7E9xRBvsJbYLFv8pbpnqjsuA
```

---

Thank you for using Prakash Perplexity Bot! 🚀

