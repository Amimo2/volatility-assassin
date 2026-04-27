class PerformanceTracker:
    """
    Tracks performance per strategy
    """

    def __init__(self):
        self.data = {}

    # --------------------------
    def _init_strategy(self, strategy):
        if strategy not in self.data:
            self.data[strategy] = {
                "total": 0,
                "wins": 0,
                "losses": 0,
                "profit": 0,
                "streak": 0,
                "best_streak": 0,
                "worst_streak": 0
            }

    # --------------------------
    def record_trade(self, strategy, result, profit):
        self._init_strategy(strategy)

        s = self.data[strategy]

        s["total"] += 1
        s["profit"] += profit

        if result == "WIN":
            s["wins"] += 1
            s["streak"] += 1
        else:
            s["losses"] += 1
            s["streak"] -= 1

        s["best_streak"] = max(s["best_streak"], s["streak"])
        s["worst_streak"] = min(s["worst_streak"], s["streak"])

    # --------------------------
    def summary(self, strategy=None):
        if strategy:
            s = self.data.get(strategy, {})
            return self._format(s)

        # all strategies
        return {
            k: self._format(v)
            for k, v in self.data.items()
        }

    # --------------------------
    def _format(self, s):
        total = s.get("total", 0)
        wins = s.get("wins", 0)

        win_rate = (wins / total * 100) if total > 0 else 0

        return {
            "trades": total,
            "wins": wins,
            "losses": s.get("losses", 0),
            "win_rate": round(win_rate, 2),
            "profit": round(s.get("profit", 0), 2),
            "best_streak": s.get("best_streak", 0),
            "worst_streak": s.get("worst_streak", 0),
        }