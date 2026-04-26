import websocket
import json
import threading
import time


class DerivAPI:
    """
    Handles connection to Deriv WebSocket API.
    Streams market data and handles auth + requests.
    """

    def __init__(self, app_id, token=None):
        self.app_id = app_id
        self.token = token
        self.ws = None
        self.is_connected = False
        self.subscriptions = {}

    # --------------------------
    # CONNECT
    # --------------------------
    def connect(self):
        url = f"wss://ws.derivws.com/websockets/v3?app_id={self.app_id}"

        self.ws = websocket.WebSocketApp(
            url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )

        thread = threading.Thread(target=self.ws.run_forever)
        thread.daemon = True
        thread.start()

        # wait for connection
        while not self.is_connected:
            time.sleep(0.1)

    # --------------------------
    # EVENTS
    # --------------------------
    def _on_open(self, ws):
        print("🔥 Connected to Deriv API")
        self.is_connected = True

        if self.token:
            self.authorize()

    def _on_message(self, ws, message):
        data = json.loads(message)

        # route messages
        if "tick" in data:
            self.handle_tick(data["tick"])

        elif "ohlc" in data:
            self.handle_candle(data["ohlc"])

        else:
            print("📩 Raw:", data)

    def _on_error(self, ws, error):
        print("⚠️ Error:", error)

    def _on_close(self, ws, close_status_code, close_msg):
        print("❌ Connection closed")

    # --------------------------
    # AUTH
    # --------------------------
    def authorize(self):
        self.send({
            "authorize": self.token
        })

    # --------------------------
    # MARKET DATA
    # --------------------------
    def subscribe_ticks(self, symbol="R_100"):
        self.send({
            "ticks": symbol,
            "subscribe": 1
        })

    def subscribe_candles(self, symbol="R_100", interval=60):
        self.send({
            "ticks_history": symbol,
            "style": "candles",
            "granularity": interval,
            "subscribe": 1
        })

    # --------------------------
    # HANDLERS (override later)
    # --------------------------
    def handle_tick(self, tick):
        print(f"📊 Tick: {tick['quote']}")

    def handle_candle(self, candle):
        print(f"🕯 Candle: O:{candle['open']} C:{candle['close']}")

    # --------------------------
    # CORE SEND METHOD
    # --------------------------
    def send(self, data):
        if self.ws:
            self.ws.send(json.dumps(data))