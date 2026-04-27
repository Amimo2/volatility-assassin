import asyncio
import os
from api.deriv_api import DerivAPI
from core.volatility import DigitAnalyzer
from core.signals import SignalGenerator
from utils.risk import RiskManager
from utils.alerts import TelegramAlert
from utils.logger import setup_logger

# =========================
# CONFIG
# =========================
APP_ID = os.getenv("DERIV_APP_ID", "YOUR_APP_ID")
TOKEN = os.getenv("DERIV_TOKEN", "YOUR_TOKEN")
SYMBOL = "1HZ100V"  # Volatility 100 (1s) — matches your screenshot
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

logger = setup_logger("main")


# =========================
# BOT CORE
# =========================
class DigitSniperBot:
    def __init__(self):
        self.api = DerivAPI(APP_ID, TOKEN)
        self.analyzer = DigitAnalyzer(buffer_size=100)  # 100-tick buffer
        self.signaler = SignalGenerator(
            strategy="OVER_1",
            barrier=1,
            confidence_threshold=0.75  # 75% confidence needed
        )
        self.risk = RiskManager(
            base_stake=10.0,      # Start small, not 3000
            max_stake=100.0,      # Cap for safety
            martingale_levels=3,  # Max 3 recovery steps
            multiplier=2.0        # 2x martingale
        )
        self.alerts = TelegramAlert(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
        self.current_trade = None
        self.is_running = False

    async def on_tick(self, tick):
        """Called on every tick."""
        price = tick["quote"]
        digit = int(str(price)[-1])
        
        # Add to analyzer
        self.analyzer.add_digit(digit)
        
        # Need minimum data
        if not self.analyzer.is_ready():
            logger.info(f"Buffering... {self.analyzer.buffer_count()}/100")
            return

        # Generate signal
        analysis = self.analyzer.analyze()
        signal = self.signaler.generate(analysis)
        
        if signal["action"] == "TRADE":
            await self.handle_signal(signal, tick)
        else:
            logger.debug(f"No signal: {signal['reason']}")

    async def handle_signal(self, signal, tick):
        """Handle trade signal — send Telegram, wait for manual confirm."""
        stake = self.risk.get_stake()
        
        trade_details = {
            "symbol": SYMBOL,
            "contract_type": "CALL",  # Over = CALL in Deriv API
            "barrier": 1,
            "duration": 1,
            "duration_unit": "t",  # ticks
            "stake": stake,
            "basis": "stake",
            "currency": "USD",
            "confidence": signal["confidence"],
            "reason": signal["reason"]
        }
        
        self.current_trade = trade_details
        
        # Send Telegram alert for manual confirmation
        message = self._format_alert(trade_details, tick)
        await self.alerts.send(message)
        
        logger.info(f"🚨 SIGNAL: {message}")

    def _format_alert(self, trade, tick):
        return (
            f"🎯 *Digit Sniper Signal*\n\n"
            f"Symbol: `{trade['symbol']}`\n"
            f"Type: *OVER 1* (1 tick)\n"
            f"Stake: `${trade['stake']:.2f}`\n"
            f"Confidence: `{trade['confidence']*100:.1f}%`\n"
            f"Reason: {trade['reason']}\n"
            f"Current Price: `{tick['quote']}`\n\n"
            f"Reply with:\n"
            f"✅ `YES` to execute\n"
            f"❌ `NO` to skip"
        )

    async def run(self):
        """Main loop."""
        self.is_running = True
        logger.info("🚀 Starting Digit Sniper Bot...")
        logger.info(f"📡 Symbol: {SYMBOL}")
        
        # Connect to Deriv
        await self.api.connect()
        
        # Subscribe to ticks
        await self.api.subscribe_ticks(SYMBOL, self.on_tick)
        
        # Keep running
        while self.is_running:
            await asyncio.sleep(1)

    def stop(self):
        self.is_running = False


# =========================
# RUN
# =========================
if __name__ == "__main__":
    bot = DigitSniperBot()
    
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
        bot.stop()