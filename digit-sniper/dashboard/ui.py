import streamlit as st
import pandas as pd
import os
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Digit Sniper LIVE", layout="wide")

# --------------------------
# AUTO REFRESH (every 2 seconds)
# --------------------------
st_autorefresh(interval=2000, key="datarefresh")

st.title("📊 Digit Sniper LIVE Dashboard 🔴")

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
# KPI SECTION
# --------------------------
col1, col2, col3 = st.columns(3)

if len(trades) > 0:
    wins = len(trades[trades["result"] == "WIN"])
    losses = len(trades[trades["result"] == "LOSS"])
    win_rate = (wins / len(trades)) * 100

    col1.metric("Total Trades", len(trades))
    col2.metric("Win Rate", f"{win_rate:.2f}%")
    col3.metric("Net Profit", f"{trades['profit'].sum():.2f}")

else:
    col1.metric("Total Trades", 0)
    col2.metric("Win Rate", "0%")
    col3.metric("Net Profit", "0")


st.divider()

# --------------------------
# LIVE SIGNAL FEED
# --------------------------
st.subheader("🎯 Live Signals")

if len(signals) > 0:
    st.dataframe(signals.tail(10), use_container_width=True)
else:
    st.warning("No signals yet")


# --------------------------
# LIVE TRADE FEED
# --------------------------
st.subheader("💰 Live Trades")

if len(trades) > 0:
    st.dataframe(trades.tail(10), use_container_width=True)
else:
    st.warning("No trades yet")


# --------------------------
# EQUITY CURVE (LIVE)
# --------------------------
st.subheader("📈 Equity Curve")

if len(trades) > 0:
    trades["cumulative_profit"] = trades["profit"].cumsum()
    st.line_chart(trades["cumulative_profit"])
else:
    st.info("Waiting for trades...")


# --------------------------
# STATUS INDICATOR
# --------------------------
st.caption("🔴 LIVE MODE ACTIVE — updates every 2 seconds")