import pandas as pd


class Analytics:
    def __init__(self, log_dir="logs"):
        self.trades_path = f"{log_dir}/trades.csv"
        self.signals_path = f"{log_dir}/signals.csv"

        self.trades = None
        self.signals = None

    # --------------------------
    def load_data(self):
        self.trades = pd.read_csv(self.trades_path)
        self.signals = pd.read_csv(self.signals_path)

    # --------------------------
    def basic_stats(self):
        total = len(self.trades)
        wins = len(self.trades[self.trades["result"] == "WIN"])
        losses = len(self.trades[self.trades["result"] == "LOSS"])

        win_rate = (wins / total * 100) if total > 0 else 0

        print("\n📊 BASIC STATS")
        print(f"Total Trades: {total}")
        print(f"Wins: {wins}")
        print(f"Losses: {losses}")
        print(f"Win Rate: {win_rate:.2f}%")

    # --------------------------
    def profit_analysis(self):
        total_profit = self.trades["profit"].sum()
        avg_profit = self.trades["profit"].mean()

        print("\n💰 PROFIT ANALYSIS")
        print(f"Total Profit: {total_profit}")
        print(f"Average Profit per Trade: {avg_profit:.2f}")

    # --------------------------
    def by_signal(self):
        print("\n🎯 PERFORMANCE BY SIGNAL")

        grouped = self.trades.groupby("signal")

        for signal, group in grouped:
            total = len(group)
            wins = len(group[group["result"] == "WIN"])
            win_rate = (wins / total * 100) if total > 0 else 0

            print(f"\n{signal}:")
            print(f"  Trades: {total}")
            print(f"  Win Rate: {win_rate:.2f}%")

    # --------------------------
    def best_barriers(self):
        print("\n📈 BEST BARRIERS")

        grouped = self.trades.groupby("barrier")

        for barrier, group in grouped:
            total = len(group)
            wins = len(group[group["result"] == "WIN"])
            win_rate = (wins / total * 100) if total > 0 else 0

            print(f"Barrier {barrier}: {win_rate:.2f}% ({total} trades)")

    # --------------------------
    def run_all(self):
        self.load_data()
        self.basic_stats()
        self.profit_analysis()
        self.by_signal()
        self.best_barriers()


# --------------------------
if __name__ == "__main__":
    analyzer = Analytics()
    analyzer.run_all()