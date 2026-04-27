class PerformanceTracker:
    """
    Tracks bot performance:
    - Wins / Losses
    - Win rate
    - Streaks
    """

    def __init__(self):
        self.total_trades = 0
        self.wins = 0
        self.losses = 0

        self.current_streak = 0
        self.best_streak = 0
        self.worst_streak = 0

    # --------------------------
    def record_trade(self, result):
        """
        result: 'WIN' or 'LOSS'
        """
        self.total_trades += 1

        if result == "WIN":
            self.wins += 1
            self.current_streak += 1
        else:
            self.losses += 1
            self.current_streak -= 1

        # update streaks
        self.best_streak = max(self.best_streak, self.current_streak)
        self.worst_streak = min(self.worst_streak, self.current_streak)

    # --------------------------
    def win_rate(self):
        if self.total_trades == 0:
            return 0
        return (self.wins / self.total_trades) * 100

    # --------------------------
    def summary(self):
        return {
            "total_trades": self.total_trades,
            "wins": self.wins,
            "losses": self.losses,
            "win_rate": round(self.win_rate(), 2),
            "best_streak": self.best_streak,
            "worst_streak": self.worst_streak
        }

from core.tracker import PerformanceTracker
    #---------------------------------------------
    self.tracker = PerformanceTracker()
self.last_signal = None