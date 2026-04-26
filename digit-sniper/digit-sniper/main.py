from api.deriv_api import DerivAPI


# =========================
# CONFIG
# =========================
APP_ID = "YOUR_APP_ID"
TOKEN = "YOUR_TOKEN"   # optional for now


# =========================
# BOT CORE
# =========================
class DigitSniperBot:
    def __init__(self):
        self.api = DerivAPI(APP_ID, TOKEN)

    def start(self):
        print("🚀 Starting Digit Sniper Bot...")

        # connect to Deriv
        self.api.connect()

        # subscribe to market data
        self.api.subscribe_ticks("R_100")       # volatility index
        self.api.subscribe_candles("R_100", 60) # 1-minute candles

        print("📡 Subscribed to market streams")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    bot = DigitSniperBot()
    bo