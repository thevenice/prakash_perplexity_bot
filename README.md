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
Bc1qqygs0fp0nhwlhuu3qam8wlmywgv0fjy86lqc4y
```

**Ethereum (ETH):**
```
0x3b03f63d7d27e2b0609306e8439cda48ed09e95a
```

**Solana (SOL):**
```
HTLDqS36vrmLLF1EbpLFYC2RMCp3eXuwisunQG32uNZH
```

**Linea:**
```
0x3b03f63d7d27e2b0609306e8439cda48ed09e95a
```

**Base:**
```
0x3b03f63d7d27e2b0609306e8439cda48ed09e95a
```

**BNB:**
```
0x3b03f63d7d27e2b0609306e8439cda48ed09e95a
```

**Sei:**
```
0x3b03f63d7d27e2b0609306e8439cda48ed09e95a
```

**OP:**
```
0x3b03f63d7d27e2b0609306e8439cda48ed09e95a
```

**Polygon (MATIC):**
```
0x3b03f63d7d27e2b0609306e8439cda48ed09e95a
```

**Arbitrum:**
```
0x3b03f63d7d27e2b0609306e8439cda48ed09e95a
```

---

Thank you for using Prakash Perplexity Bot! 🚀

