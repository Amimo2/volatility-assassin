from collections import deque


class SignalEngine:
    """
    Converts raw market ticks into simple trading signals.
    Phase 1: digit-based momentum logic (simple + expandable)
    """

    def __init__(self, window_size=20):
        self.prices = deque(maxlen=window_size)
        self.digits = deque(maxlen=window_size)

    # --------------------------
    # PROCESS INCOMING TICK
    # --------------------------
    def add_tick(self, price):
        self.prices.append(price)

        digit = int(str(price)[-1])
        self.digits.append(digit)

        return self.generate_signal()

    # --------------------------
    # CORE LOGIC (PHASE 1)
    # --------------------------
    def generate_signal(self):
        if len(self.digits) < 10:
            return "WAIT"

        # count digit frequency
        freq = {}
        for d in self.digits:
            freq[d] = freq.get(d, 0) + 1

        most_common_digit = max(freq, key=freq.get)
        least_common_digit = min(freq, key=freq.get)

        last_digit = self.digits[-1]

        # --------------------------
        # SIMPLE SNIPER RULES
        # --------------------------

        # 🔥 reversal signal
        if last_digit == least_common_digit:
            return "BUY"

        # 🔻 exhaustion signal
        if last_digit == most_common_digit:
            return "SELL"

        return "WAIT"

    # --------------------------
    # DEBUG VIEW
    # --------------------------
    def debug(self):
        return {
            "prices": list(self.prices),
            "digits": list(self.digits),
        }