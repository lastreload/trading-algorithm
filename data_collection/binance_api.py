import os
import sys

# Aggiunge il percorso della cartella superiore alla sys.path per poter importare config.py
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import logging
from binance.client import Client
import config

# Configura il logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Inizializza il client di Binance usando le API key definite in config.py
client = Client(config.BINANCE_API_KEY, config.BINANCE_SECRET_KEY)

def get_current_price(symbol="BTCUSDT"):
    """
    Recupera il prezzo corrente per il simbolo specificato.
    """
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        logging.info("Prezzo corrente ottenuto per %s", symbol)
        return ticker
    except Exception as e:
        logging.error("Errore nel recupero del prezzo per %s: %s", symbol, e)
        return None

def get_historical_klines(symbol="BTCUSDT", interval="1h", limit=100):
    """
    Recupera dati storici (klines) per il simbolo specificato.
    Il parametro 'interval' può essere '1m', '1h', '1d', ecc.
    Il parametro 'limit' definisce quanti dati recuperare.
    """
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        logging.info("Dati storici ottenuti per %s", symbol)
        return klines
    except Exception as e:
        logging.error("Errore nel recupero dei dati storici per %s: %s", symbol, e)
        return None

if __name__ == "__main__":
    # Test della funzione per ottenere il prezzo corrente
    ticker = get_current_price("BTCUSDT")
    if ticker:
        print("Prezzo corrente BTC/USDT:", ticker)
    
    # Test della funzione per ottenere i dati storici
    klines = get_historical_klines("BTCUSDT", interval="1h", limit=10)
    if klines:
        print("Dati storici (primi 10):")
        for k in klines:
            print(k)
