class StrategyRecovery:
    def __init__(self):
        self.recovery_data = {}

        # thresholds
        self.min_trades = 20
        self.min_win_rate = 55

    # --------------------------
    def track(self, strategy, result, profit):
        if strategy not in self.recovery_data:
            self.recovery_data[strategy] = {
                "trades": 0,
                "wins": 0,
                "profit": 0
            }

        data = self.recovery_data[strategy]

        data["trades"] += 1
        data["profit"] += profit

        if result == "WIN":
            data["wins"] += 1

    # --------------------------
    def check_recovery(self, strategy):
        data = self.recovery_data.get(strategy)

        if not data:
            return False

        trades = data["trades"]
        wins = data["wins"]
        profit = data["profit"]

        if trades < self.min_trades:
            return False

        win_rate = (wins / trades) * 100

        if win_rate >= self.min_win_rate and profit > 0:
            print(f"♻️ Strategy RECOVERED: {strategy}")
            return True

        return False

    # --------------------------
    def reset(self, strategy):
        if strategy in self.recovery_data:
            del self.recovery_data[strategy]