from collections import deque


class MomentumFilter:
    def __init__(self, window=5):
        self.prices = deque(maxlen=window)

    def add_price(self, price):
        self.prices.append(price)

    def get_momentum(self):
        if len(self.prices) < 3:
            return "FLAT"

        increases = 0
        decreases = 0

        for i in range(1, len(self.prices)):
            if self.prices[i] > self.prices[i - 1]:
                increases += 1
            elif self.prices[i] < self.prices[i - 1]:
                decreases += 1

        if increases > decreases:
            return "UP"
        elif decreases > increases:
            return "DOWN"

        return "FLAT"