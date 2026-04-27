from collections import deque


class SignalEngine:
    """
    OVER / UNDER Digit Sniper Engine
    - Tracks digit distribution
    - Generates probability-based signals
    - Adds confidence scoring
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
    # CORE SNIPER LOGIC
    # --------------------------
    def generate_signal(self):
        if len(self.digits) < 15:
            return {"signal": "WAIT", "confidence": 0}

        # classify digits
        low_digits = [0, 1, 2, 3, 4]
        high_digits = [5, 6, 7, 8, 9]

        low_count = sum(1 for d in self.digits if d in low_digits)
        high_count = sum(1 for d in self.digits if d in high_digits)

        total = len(self.digits)

        low_prob = low_count / total
        high_prob = high_count / total

        last_digit = self.digits[-1]

        # --------------------------
        # CONFIDENCE CALCULATION
        # --------------------------
        confidence = abs(high_prob - low_prob) * 100

        # --------------------------
        # SIGNAL RULES
        # --------------------------

        # OVER condition (high digits dominance expected)
        if high_prob > low_prob and confidence > 10:
            return {
                "signal": "OVER",
                "confidence": round(confidence, 2),
                "last_digit": last_digit
            }

        # UNDER condition (low digits dominance expected)
        if low_prob > high_prob and confidence > 10:
            return {
                "signal": "UNDER",
                "confidence": round(confidence, 2),
                "last_digit": last_digit
            }

        # no edge
        return {
            "signal": "WAIT",
            "confidence": round(confidence, 2),
            "last_digit": last_digit
        }

    # --------------------------
    # DEBUG VIEW
    # --------------------------
    def debug(self):
        return {
            "prices": list(self.prices),
            "digits": list(self.digits),
        }