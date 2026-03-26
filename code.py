# Prototype: SMA Crossover Strategy Visualization
# Save this as notebooks/prototype.ipynb

import os
import pandas as pd
import matplotlib.pyplot as plt
from binance.client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Initialize Binance client (testnet mode)
client = Client(API_KEY, API_SECRET, testnet=True)

# Fetch historical candlestick data
klines = client.futures_klines(symbol="BTCUSDT", interval="1h", limit=200)
df = pd.DataFrame(klines, columns=[
    "time","open","high","low","close","volume",
    "close_time","quote_asset_volume","trades",
    "taker_buy_base","taker_buy_quote","ignore"
])
df["time"] = pd.to_datetime(df["time"], unit="ms")
df["close"] = df["close"].astype(float)

# Calculate SMAs
df["SMA50"] = df["close"].rolling(50).mean()
df["SMA200"] = df["close"].rolling(200).mean()

# Plot candlesticks + SMAs
plt.figure(figsize=(12,6))
plt.plot(df["time"], df["close"], label="Close Price", color="black")
plt.plot(df["time"], df["SMA50"], label="SMA50", color="blue")
plt.plot(df["time"], df["SMA200"], label="SMA200", color="red")
plt.title("BTCUSDT Futures Testnet - SMA Crossover Strategy")
plt.xlabel("Time")
plt.ylabel("Price (USDT)")
plt.legend()
plt.grid(True)
plt.show()

# Signal
if df["SMA50"].iloc[-1] > df["SMA200"].iloc[-1]:
    print("Signal: LONG")
else:
    print("Signal: SHORT")
