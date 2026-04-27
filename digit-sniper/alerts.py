import requests


class AlertSystem:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    # --------------------------
    def send_message(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        payload = {
            "chat_id": self.chat_id,
            "text": message
        }

        try:
            requests.post(url, data=payload)
        except Exception as e:
            print("⚠️ Alert failed:", e)

    # --------------------------
    def signal_alert(self, signal, confidence, barrier):
        msg = f"""
🚨 DIGIT SNIPER ALERT

🎯 Signal: {signal}
📊 Confidence: {confidence}%
📍 Barrier: {barrier}
        """
        self.send_message(msg)

    # --------------------------
    def trade_alert(self, result, profit):
        emoji = "💰" if result == "WIN" else "❌"

        msg = f"""
{emoji} TRADE RESULT

Result: {result}
Profit: {profit}
        """
        self.send_message(msg)