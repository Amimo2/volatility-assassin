import streamlit as st
import pandas as pd
import os


st.set_page_config(page_title="Digit Sniper Dashboard", layout="wide")

st.title("📊 Digit Sniper Dashboard")


# --------------------------
# LOAD DATA
# --------------------------
def load_data():
    trades_path = "logs/trades.csv"
    signals_path = "logs/signals.csv"

    trades = pd.read_csv(trades_path) if os.path.exists(trades_path) else pd.DataFrame()
    signals = pd.read_csv(signals_path) if os.path.exists(signals_path) else pd.DataFrame()

    return trades, signals


trades, signals = load_data()


# --------------------------
# KPIs
# --------------------------
col1, col2, col3 = st.columns(3)

if len(trades) > 0:
    wins = len(trades[trades["result"] == "WIN"])
    losses = len(trades[trades["result"] == "LOSS"])
    win_rate = (wins / len(trades)) * 100

    col1.metric("Total Trades", len(trades))
    col2.metric("Win Rate", f"{win_rate:.2f}%")
    col3.metric("Net Profit", trades["profit"].sum())

else:
    col1.metric("Total Trades", 0)
    col2.metric("Win Rate", "0%")
    col3.metric("Net Profit", 0)


st.divider()


# --------------------------
# TRADE HISTORY
# --------------------------
st.subheader("💰 Trade History")

if len(trades) > 0:
    st.dataframe(trades.tail(20), use_container_width=True)
else:
    st.warning("No trade data yet")


# --------------------------
# SIGNAL HISTORY
# --------------------------
st.subheader("🎯 Signal History")

if len(signals) > 0:
    st.dataframe(signals.tail(20), use_container_width=True)
else:
    st.warning("No signal data yet")


# --------------------------
# CHARTS
# --------------------------
st.subheader("📈 Performance Chart")

if len(trades) > 0:
    trades["cumulative_profit"] = trades["profit"].cumsum()
    st.line_chart(trades["cumulative_profit"])
else:
    st.info("Waiting for data...")


# --------------------------
# REFRESH NOTE
# --------------------------
st.caption("Refresh page to update live data")