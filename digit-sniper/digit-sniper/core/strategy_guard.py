class StrategyGuard:
    def __init__(self):
        self.disabled = set()

        # thresholds (tune later)
        self.min_trades = 30
        self.min_win_rate = 50
        self.max_loss_streak = -5

    # --------------------------
    def evaluate(self, tracker):
        summaries = tracker.summary()

        for strategy, stats in summaries.items():

            trades = stats["trades"]
            win_rate = stats["win_rate"]
            profit = stats["profit"]
            streak = stats["worst_streak"]

            # skip if not enough data
            if trades < self.min_trades:
                continue

            # disable conditions
            if (
                win_rate < self.min_win_rate
                or profit < 0
                or streak <= self.max_loss_streak
            ):
                self.disabled.add(strategy)
                print(f"🛑 Strategy DISABLED: {strategy}")

    # --------------------------
    def is_enabled(self, strategy):
        return strategy not in self.disabled

    # --------------------------
    def reset(self):
        self.disabled.clear()