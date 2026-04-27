class RiskManager:
    """
    Controls trading risk:
    - stake sizing
    - max loss limit
    - profit target
    - streak protection
    """

    def __init__(self):
        self.balance = 100  # demo starting balance

        self.base_stake = 1
        self.current_stake = self.base_stake

        self.max_loss = 20
        self.profit_target = 30

        self.total_profit = 0
        self.loss_streak = 0

    # --------------------------
    def can_trade(self):
        if self.total_profit <= -self.max_loss:
            return False, "Max loss reached"

        if self.total_profit >= self.profit_target:
            return False, "Profit target reached"

        if self.loss_streak >= 3:
            return False, "Loss streak limit reached"

        return True, "OK"

    # --------------------------
    def get_stake(self):
        return self.current_stake

    # --------------------------
    def update_after_trade(self, result):
        if result == "WIN":
            self.total_profit += self.current_stake
            self.loss_streak = 0
            self.current_stake = self.base_stake

        else:
            self.total_profit -= self.current_stake
            self.loss_streak += 1

            # simple recovery (optional)
            self.current_stake = min(self.current_stake * 2, 10)

    # --------------------------
    def summary(self):
        return {
            "balance": self.balance,
            "profit": self.total_profit,
            "loss_streak": self.loss_streak,
            "current_stake": self.current_stake
        }