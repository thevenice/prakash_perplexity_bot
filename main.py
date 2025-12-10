import os
import time
import requests
import asyncio
from datetime import datetime, timedelta
from telegram import Bot
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ========= CONFIG =========
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")      # from BotFather
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")          # your chat / channel id
if TELEGRAM_CHAT_ID:
    try:
        TELEGRAM_CHAT_ID = int(TELEGRAM_CHAT_ID)
    except ValueError:
        pass  # Keep as string if it's not a valid integer
PPLX_API_KEY = os.getenv("PPLX_API_KEY")                  # from Perplexity Settings → API
MARKET_API_KEY = os.getenv("MARKET_API_KEY")              # e.g. Alpha Vantage / Polygon key

# symbols you care about
WATCHLIST = ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "AAPL", "NVDA"]

# polling interval in seconds
POLL_INTERVAL = 300  # 5 minutes

# simple thresholds you can tune
MIN_ABS_PCT_MOVE = 1.5  # only consider moves above this in percent

# ========= HELPERS =========

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def get_latest_price(symbol):
    """
    Uses Finnhub's /quote endpoint for real-time prices.
    symbol example: 'AAPL', 'BINANCE:BTCUSDT'
    """
    url = "https://finnhub.io/api/v1/quote"
    params = {
        "symbol": symbol,
        "token": FINNHUB_API_KEY,
    }
    for attempt in range(3):
        try:
            r = requests.get(url, params=params, timeout=20)
            r.raise_for_status()
            data = r.json()
            # c = current price, pc = previous close, per Finnhub docs
            price = float(data.get("c", 0.0))
            prev_close = float(data.get("pc", 0.0))
            if price == 0 or prev_close == 0:
                return None, None
            pct_change = (price - prev_close) / prev_close * 100.0
            return price, pct_change
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            if attempt == 2:
                raise
            time.sleep(1)


def analyze_trends_with_perplexity(market_snapshot):
    """
    market_snapshot: list of dicts, each with {symbol, price, pct_change}
    Calls Perplexity API to decide which symbols deserve alerts and why.
    """
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PPLX_API_KEY}",
        "Content-Type": "application/json",
    }

    prompt = (
        "You are an assistant for market monitoring.\n"
        "You receive a JSON array of tickers with current price and percent change vs previous close.\n"
        "Identify only the most notable short-term moves that should trigger an alert for an active trader.\n"
        "Return a JSON list of objects with fields: symbol, should_alert (true/false), "
        "reason (short one-line explanation), sentiment ('bullish'|'bearish'|'unclear').\n"
        "Be selective and avoid noise.\n\n"
        f"Data: {market_snapshot}"
    )

    payload = {
        "model": "sonar-pro",   # choose the model available to your API key
        "messages": [
            {"role": "system", "content": "You are a quantitative trading assistant."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 512,
        "temperature": 0.2,
    }

    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    content = r.json()["choices"][0]["message"]["content"]

    # Perplexity returns text; expect it to be JSON and eval via json.loads
    import json
    try:
        alerts = json.loads(content)
    except json.JSONDecodeError:
        # fallback: no alerts if parsing fails
        alerts = []
    return alerts


def format_alert_message(alerts):
    """
    Turn Perplexity's structured alerts into a Telegram-friendly message.
    """
    if not alerts:
        return None

    lines = ["📈 Market trend alerts:"]
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines.append(f"Time: {now}")
    lines.append("")

    for a in alerts:
        if not a.get("should_alert"):
            continue
        symbol = a.get("symbol")
        reason = a.get("reason", "")
        sentiment = a.get("sentiment", "unclear")
        emoji = "🟢" if sentiment == "bullish" else "🔴" if sentiment == "bearish" else "⚪️"
        lines.append(f"{emoji} {symbol}: {reason}")

    # if nothing passed the filter, return None
    meaningful = [a for a in alerts if a.get("should_alert")]
    if not meaningful:
        return None

    return "\n".join(lines)


def send_telegram_message(text):
    """Send a message to Telegram using async API"""
    async def _send():
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        try:
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text, parse_mode=None)
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
            raise
        finally:
            await bot.close()
    
    try:
        asyncio.run(_send())
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")
        raise


# ========= MAIN LOOP =========

def main():
    if not (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID and PPLX_API_KEY and FINNHUB_API_KEY):
        raise RuntimeError("Missing environment variables. Set TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, PPLX_API_KEY, FINNHUB_API_KEY.")

    print("Starting market trend alert bot...")

    while True:
        snapshot = []
        for symbol in WATCHLIST:
            try:
                price, pct = get_latest_price(symbol)
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                continue

            if price is None:
                continue

            # pre-filter: ignore tiny moves
            if abs(pct) < MIN_ABS_PCT_MOVE:
                continue

            snapshot.append({
                "symbol": symbol,
                "price": round(price, 4),
                "pct_change": round(pct, 3),
            })

        if snapshot:
            try:
                alerts = analyze_trends_with_perplexity(snapshot)
                msg = format_alert_message(alerts)
                if msg:
                    send_telegram_message(msg)
                    print(f"Sent alert:\n{msg}")
                else:
                    print("No meaningful alerts this cycle.")
            except Exception as e:
                print(f"Error in analysis/alert cycle: {e}")
        else:
            print("No symbols passed movement threshold.")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
