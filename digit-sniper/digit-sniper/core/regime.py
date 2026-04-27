class MarketRegime:
    def __init__(self, momentum_filter, volatility_filter):
        self.momentum = momentum_filter
        self.volatility = volatility_filter

    # --------------------------
    def detect(self):
        vol = self.volatility.get_volatility()
        mom = self.momentum.get_momentum()

        # --------------------------
        # DEAD MARKET
        # --------------------------
        if vol < 0.2:
            return "DEAD"

        # --------------------------
        # CHAOTIC (too fast)
        # --------------------------
        if vol > 2:
            return "CHAOTIC"

        # --------------------------
        # TREND
        # --------------------------
        if mom in ["UP", "DOWN"]:
            return "TREND"

        # --------------------------
        # RANGE
        # --------------------------
        return "RANGE"