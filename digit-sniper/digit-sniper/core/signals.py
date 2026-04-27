from collections import deque


class SignalEngine:
    """
    OVER / UNDER Sniper with Trend Filter
    - Digit probability
    - Market trend filter
    - Confidence scoring
    """

    def __init__(self, window_size=30):
        self.prices = deque(maxlen=window_size)
        self.digits = deque(maxlen=window_size)

    # --------------------------
    # INPUT STREAM
    # --------------------------
    def add_tick(self, price):
        self.prices.append(price)

        digit = int(str(price)[-1])
        self.digits.append(digit)

        return self.generate_signal()

    # --------------------------
    # TREND DETECTION
    # --------------------------
    def get_trend(self):
        if len(self.prices) < 10:
            return "FLAT"

        # simple trend: compare recent avg vs older avg
        recent = list(self.prices)[-5:]
        older = list(self.prices)[:5]

        recent_avg = sum(recent) / len(recent)
        older_avg = sum(older) / len(older)

        if recent_avg > older_avg:
            return "UP"
        elif recent_avg < older_avg:
            return "DOWN"
        else:
            return "FLAT"

    # --------------------------
    # CORE LOGIC
    # --------------------------
    def generate_signal(self):
        if len(self.digits) < 15:
            return {"signal": "WAIT", "confidence": 0}

        # digit zones
        low_digits = [0, 1, 2, 3, 4]
        high_digits = [5, 6, 7, 8, 9]

        low_count = sum(1 for d in self.digits if d in low_digits)
        high_count = sum(1 for d in self.digits if d in high_digits)

        total = len(self.digits)

        low_prob = low_count / total
        high_prob = high_count / total

        # trend
        trend = self.get_trend()

        # confidence
        base_conf = abs(high_prob - low_prob) * 100

        # --------------------------
        # FILTERED SIGNAL LOGIC
        # --------------------------

        # OVER (only if trend supports)
        if high_prob > low_prob and trend == "UP" and base_conf > 10:
            return {
                "signal": "OVER",
                "confidence": round(base_conf + 10, 2),  # boost
                "trend": trend
            }

        # UNDER (only if trend supports)
        if low_prob > high_prob and trend == "DOWN" and base_conf > 10:
            return {
                "signal": "UNDER",
                "confidence": round(base_conf + 10, 2),
                "trend": trend
            }

        # weak / conflict
        return {
            "signal": "WAIT",
            "confidence": round(base_conf, 2),
            "trend": trend
        }

    # --------------------------
    # DEBUG
    # --------------------------
    def debug(self):
        return {
            "prices": list(self.prices),
            "digits": list(self.digits),
        }
        active = self.engine.get_active()

for name, result in signals.items():

    signal = result.get("signal")

    if signal != "OVER":
        continue

    # only active strategy trades real money
    if name != active:
        print(f"👀 Paper mode: {name}")
        continue

    # check guard
    if not self.strategy_guard.is_enabled(name):
        print(f"⛔ Disabled: {name}")
        continue

    # filters
    can_trade, reason = self.volatility.is_tradeable()
    if not can_trade:
        return

    if self.momentum.get_momentum() != "UP":
        return

    print(f"🚀 REAL TRADE → {name}")

    self.current_trade = {
        "strategy": name,
        "signal": "OVER",
        "barrier": 1,
        "stake": self.risk.get_stake()
    }

    self.api.buy_contract(
        symbol="R_100",
        contract_type="DIGITOVER",
        barrier=1,
        amount=self.current_trade["stake"]
    )
    active = self.engine.get_active()

for name, result in signals.items():

    signal = result.get("signal")
    barrier = result.get("barrier", 1)

    if signal not in ["OVER", "UNDER"]:
        continue

    # only best strategy trades
    if name != active:
        print(f"👀 Paper mode: {name}")
        continue

    if not self.strategy_guard.is_enabled(name):
        print(f"⛔ Disabled: {name}")
        continue

    # --------------------------
    # Volatility filter
    # --------------------------
    can_trade, reason = self.volatility.is_tradeable()
    if not can_trade:
        return

    # --------------------------
    # Momentum filter
    # --------------------------
    momentum = self.momentum.get_momentum()

    if signal == "OVER" and momentum != "UP":
        return

    if signal == "UNDER" and momentum != "DOWN":
        return

    print(f"🚀 REAL TRADE → {name} ({signal})")

    self.current_trade = {
        "strategy": name,
        "signal": signal,
        "barrier": barrier,
        "stake": self.risk.get_stake()
    }

    contract_type = "DIGITOVER" if signal == "OVER" else "DIGITUNDER"

    self.api.buy_contract(
        symbol="R_100",
        contract_type=contract_type,
        barrier=barrier,
        amount=self.current_trade["stake"]
    )