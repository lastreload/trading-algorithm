# Soluzione per ModuleNotFoundError in preprocessing/data_cleaning.py
import os
import sys

# Aggiungi il percorso della cartella principale del progetto a sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Ora è possibile importare il modulo data_collection
from data_collection.binance_api import get_historical_klines
import pandas as pd

def clean_data(klines):
    """
    Converte la lista di klines in un DataFrame Pandas e normalizza i dati.
    Le colonne del DataFrame saranno:
      - open_time, open, high, low, close, volume, close_time, quote_asset_volume,
        num_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, ignore
    """
    columns = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ]
    df = pd.DataFrame(klines, columns=columns)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col])
        
    return df

def compute_SMA(df, window=20):
    """
    Calcola la media mobile semplice (SMA) per la colonna 'close' del DataFrame.
    """
    df["SMA"] = df["close"].rolling(window=window).mean()
    return df

if __name__ == "__main__":
    # Recupera i dati storici per BTCUSDT
    klines = get_historical_klines(symbol="BTCUSDT", interval="1h", limit=100)
    if klines:
        df = clean_data(klines)
        df = compute_SMA(df, window=20)
        print(df.head())
