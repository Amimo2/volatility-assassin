from api.deriv_api import DerivAPI
from core.signals import SignalEngine


# =========================
# CONFIG
# =========================
APP_ID = "YOUR_APP_ID"
TOKEN = "YOUR_TOKEN"


# =========================
# BOT CORE
# =========================
class DigitSniperBot:
    def __init__(self):
        self.api = DerivAPI(APP_ID, TOKEN)
        self.signals = SignalEngine()

    def start(self):
        print("🚀 Digit Sniper Bot Starting...")

        # override API handlers BEFORE connect
        self.api.handle_tick = self.on_tick
        self.api.handle_candle = self.on_candle

        # connect + subscribe
        self.api.connect()
        self.api.subscribe_ticks("R_100")
        self.api.subscribe_candles("R_100", 60)

        print("📡 Market streams active")

    # --------------------------
    # TICK HANDLER (CORE PIPELINE)
    # --------------------------
    def on_tick(self, tick):
        price = float(tick["quote"])

        signal = self.signals.add_tick(price)

        print(f"📊 Price: {price} | 🎯 Signal: {signal}")

    # --------------------------
    # CANDLE HANDLER (optional for later)
    # --------------------------
    def on_candle(self, candle):
        print(f"🕯 Candle closed: {candle['close']}")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    bot = DigitSniperBot()
    bot.start()