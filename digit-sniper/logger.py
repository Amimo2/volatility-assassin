import csv
import os
from datetime import datetime


class BotLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir

        os.makedirs(self.log_dir, exist_ok=True)

        self.signal_file = os.path.join(log_dir, "signals.csv")
        self.trade_file = os.path.join(log_dir, "trades.csv")

        self._init_files()

    # --------------------------
    def _init_files(self):
        # create files with headers if not exist
        if not os.path.exists(self.signal_file):
            with open(self.signal_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "time", "price", "signal", "confidence", "trend"
                ])

        if not os.path.exists(self.trade_file):
            with open(self.trade_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "time", "signal", "barrier", "stake", "result", "profit"
                ])

    # --------------------------
    def log_signal(self, price, signal_data):
        with open(self.signal_file, "a", newline="") as f:
            writer = csv.writer(f)

            writer.writerow([
                datetime.now().isoformat(),
                price,
                signal_data.get("signal"),
                signal_data.get("confidence"),
                signal_data.get("trend")
            ])

    # --------------------------
    def log_trade(self, signal, barrier, stake, result, profit):
        with open(self.trade_file, "a", newline="") as f:
            writer = csv.writer(f)

            writer.writerow([
                datetime.now().isoformat(),
                signal,
                barrier,
                stake,
                result,
                profit
            ])