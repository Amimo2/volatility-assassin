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
    bot.start()

    self.current_trade = {
    "strategy": "ZERO_ONE",
    "signal": "OVER",
    "barrier": 1,
    "stake": self.risk.get_stake()
}
from core.strategy_guard import StrategyGuard
from core.recovery import StrategyRecovery
class ZeroOneCounter:
    def __init__(self):
        self.buffer = []

    def process(self, price):
        digit = int(str(price)[-1])

        self.buffer.append(digit)

        if len(self.buffer) > 5:
            self.buffer.pop(0)

        if len(self.buffer) < 4:
            return {"signal": "WAIT"}

        # count 0/1 cluster
        cluster = sum(1 for d in self.buffer if d in [0, 1])

        # detect unstable clustering
        if cluster >= 3:
            return {
                "signal": "UNDER",
                "barrier": 1,
                "entry": "COUNTER"
            }

        return {"signal": "WAIT"}