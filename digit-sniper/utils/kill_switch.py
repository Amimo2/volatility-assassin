class KillSwitch:
    """
    Emergency protection system for bot safety
    """

    def __init__(self):
        self.enabled = True

        self.max_drawdown = -20   # stop if losses exceed
        self.min_win_rate = 45    # safety threshold

    # --------------------------
    def evaluate(self, tracker):
        """
        tracker = PerformanceTracker()
        """

        stats = tracker.summary()

        win_rate = stats["win_rate"]
        profit = stats["profit"]
        streak = stats["loss_streak"]

        # --------------------------
        # CONDITIONS
        # --------------------------

        if profit <= self.max_drawdown:
            self.enabled = False
            return "STOP: Max drawdown hit"

        if win_rate < self.min_win_rate and stats["total_trades"] > 20:
            self.enabled = False
            return "STOP: Low win rate"

        if streak <= -4:
            self.enabled = False
            return "STOP: Losing streak too deep"

        return "OK"

    # --------------------------
    def can_trade(self):
        return self.enabled

    # --------------------------
    def force_stop(self):
        self.enabled = False

    def reset(self):
        self.enabled = True