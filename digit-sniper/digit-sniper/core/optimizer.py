import pandas as pd


class StrategyOptimizer:
    def __init__(self, log_dir="logs"):
        self.trades_path = f"{log_dir}/trades.csv"

    def load_data(self):
        return pd.read_csv(self.trades_path)

    # --------------------------
    def best_signal(self, df):
        grouped = df.groupby("signal")

        results = {}

        for signal, group in grouped:
            total = len(group)
            wins = len(group[group["result"] == "WIN"])
            win_rate = (wins / total * 100) if total > 0 else 0

            results[signal] = win_rate

        return results

    # --------------------------
    def best_barrier(self, df):
        grouped = df.groupby("barrier")

        best = None
        best_rate = 0

        for barrier, group in grouped:
            total = len(group)
            if total < 10:
                continue  # ignore low data

            wins = len(group[group["result"] == "WIN"])
            win_rate = (wins / total * 100)

            if win_rate > best_rate:
                best_rate = win_rate
                best = barrier

        return best, best_rate

    # --------------------------
    def optimize(self):
        df = self.load_data()

        signal_perf = self.best_signal(df)
        best_barrier, barrier_rate = self.best_barrier(df)

        config = {
            "enabled_signals": [],
            "best_barrier": best_barrier,
            "barrier_winrate": round(barrier_rate, 2)
        }

        # enable only strong signals (>55%)
        for sig, rate in signal_perf.items():
            if rate >= 55:
                config["enabled_signals"].append(sig)

        return config