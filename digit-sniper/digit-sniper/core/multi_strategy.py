class MultiStrategyEngine:
    def __init__(self):
        self.strategies = {}
        self.active_strategy = None

        # thresholds
        self.min_trades = 30

    # --------------------------
    def register(self, name, strategy):
        self.strategies[name] = strategy

    # --------------------------
    def evaluate(self, tracker):
        summaries = tracker.summary()

        best = None
        best_score = -999

        for name, stats in summaries.items():
            if stats["trades"] < self.min_trades:
                continue

            # simple scoring
            score = stats["win_rate"] + stats["profit"]

            if score > best_score:
                best_score = score
                best = name

        self.active_strategy = best

        if best:
            print(f"🏆 Active Strategy: {best}")

    # --------------------------
    def get_active(self):
        return self.active_strategy

    # --------------------------
    def run(self, price):
        signals = {}

        for name, strat in self.strategies.items():
            result = strat.process(price)
            signals[name] = result

        return signals