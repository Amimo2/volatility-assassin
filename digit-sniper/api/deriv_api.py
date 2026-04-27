import asyncio
import json
import websockets
from typing import Callable, Optional, Dict, Any
from utils.logger import setup_logger

logger = setup_logger("deriv_api")


class DerivAPI:
    """
    Deriv WebSocket API client for Volatility Index trading.
    Handles connection, tick streaming, and contract requests.
    """
    
    DERIV_WS_URL = "wss://ws.derivws.com/websockets/v3?app_id={app_id}"
    
    def __init__(self, app_id: str, token: Optional[str] = None):
        self.app_id = app_id
        self.token = token
        self.ws = None
        self.is_connected = False
        self.message_handlers: Dict[str, Callable] = {}
        self.tick_callbacks: Dict[str, Callable] = {}
        self.req_id = 0
        self._listen_task = None
        
    def _get_req_id(self) -> int:
        """Generate unique request ID."""
        self.req_id += 1
        return self.req_id
    
    async def connect(self) -> bool:
        """
        Establish WebSocket connection to Deriv.
        Returns True if successful.
        """
        url = self.DERIV_WS_URL.format(app_id=self.app_id)
        
        try:
            logger.info(f"Connecting to Deriv: {url}")
            self.ws = await websockets.connect(url)
            self.is_connected = True
            
            # Start listener task
            self._listen_task = asyncio.create_task(self._listen())
            
            # Authorize if token provided
            if self.token:
                await self.authorize()
            
            logger.info("✅ Connected to Deriv WebSocket")
            return True
            
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            self.is_connected = False
            return False
    
    async def authorize(self):
        """Authorize with API token."""
        req_id = self._get_req_id()
        auth_msg = {
            "authorize": self.token,
            "req_id": req_id
        }
        await self.ws.send(json.dumps(auth_msg))
        logger.info("Authorizing...")
        
        # Wait for response (handled in _listen)
        await asyncio.sleep(0.5)
    
    async def _listen(self):
        """
        Main listener loop. Handles incoming messages and routes them
        to appropriate callbacks.
        """
        while self.is_connected and self.ws:
            try:
                msg = await self.ws.recv()
                data = json.loads(msg)
                
                # Route by message type
                if "tick" in data:
                    await self._handle_tick(data["tick"])
                elif "proposal" in data:
                    await self._handle_proposal(data)
                elif "buy" in data:
                    await self._handle_buy(data)
                elif "error" in data:
                    logger.error(f"API Error: {data['error']}")
                elif "authorize" in data:
                    logger.info("✅ Authorized successfully")
                    
            except websockets.exceptions.ConnectionClosed:
                logger.warning("WebSocket connection closed")
                self.is_connected = False
                break
            except Exception as e:
                logger.error(f"Listener error: {e}")
    
    async def _handle_tick(self, tick: Dict[str, Any]):
        """Route tick data to subscribed callbacks."""
        symbol = tick.get("symbol", "")
        if symbol in self.tick_callbacks:
            await self.tick_callbacks[symbol](tick)
    
    async def _handle_proposal(self, data: Dict):
        """Handle proposal response."""
        req_id = data.get("req_id")
        if req_id and req_id in self.message_handlers:
            handler = self.message_handlers.pop(req_id)
            await handler(data)
    
    async def _handle_buy(self, data: Dict):
        """Handle buy response."""
        req_id = data.get("req_id")
        if req_id and req_id in self.message_handlers:
            handler = self.message_handlers.pop(req_id)
            await handler(data)
    
    async def subscribe_ticks(self, symbol: str, callback: Callable):
        """
        Subscribe to tick stream for a symbol.
        
        Args:
            symbol: e.g., "1HZ100V" (Volatility 100 1s), "1HZ75V", "R_100"
            callback: async function(tick_dict) to call on each tick
        """
        if not self.is_connected:
            raise ConnectionError("Not connected to Deriv")
        
        self.tick_callbacks[symbol] = callback
        
        req_id = self._get_req_id()
        msg = {
            "ticks": symbol,
            "subscribe": 1,
            "req_id": req_id
        }
        
        await self.ws.send(json.dumps(msg))
        logger.info(f"📡 Subscribed to ticks: {symbol}")
    
    async def unsubscribe_ticks(self, symbol: str):
        """Unsubscribe from tick stream."""
        req_id = self._get_req_id()
        msg = {
            "ticks": symbol,
            "subscribe": 0,
            "req_id": req_id
        }
        await self.ws.send(json.dumps(msg))
        
        if symbol in self.tick_callbacks:
            del self.tick_callbacks[symbol]
        
        logger.info(f"Unsubscribed from ticks: {symbol}")
    
    async def get_proposal(self, contract_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get contract proposal (price quote) before buying.
        
        For Over/Under 1 tick:
        {
            "contract_type": "CALL",  # Over = CALL
            "symbol": "1HZ100V",
            "duration": 1,
            "duration_unit": "t",
            "barrier": 1,
            "basis": "stake",
            "currency": "USD",
            "amount": 10
        }
        """
        req_id = self._get_req_id()
        
        proposal_msg = {
            "proposal": 1,
            "req_id": req_id,
            **contract_params
        }
        
        # Set up future to capture response
        future = asyncio.Future()
        
        def handler(data):
            if not future.done():
                future.set_result(data)
        
        self.message_handlers[req_id] = handler
        
        await self.ws.send(json.dumps(proposal_msg))
        logger.debug(f"Sent proposal request: {req_id}")
        
        # Wait for response with timeout
        try:
            result = await asyncio.wait_for(future, timeout=5.0)
            return result
        except asyncio.TimeoutError:
            logger.error("Proposal request timed out")
            return {"error": "timeout"}
    
    async def buy_contract(self, proposal_id: str, price: float) -> Dict[str, Any]:
        """
        Buy a contract using proposal ID.
        
        Args:
            proposal_id: ID from get_proposal response
            price: Maximum price to pay (stake amount)
        """
        req_id = self._get_req_id()
        
        buy_msg = {
            "buy": proposal_id,
            "price": price,
            "req_id": req_id
        }
        
        future = asyncio.Future()
        
        def handler(data):
            if not future.done():
                future.set_result(data)
        
        self.message_handlers[req_id] = handler
        
        await self.ws.send(json.dumps(buy_msg))
        logger.info(f"💰 Buying contract: proposal_id={proposal_id}, price={price}")
        
        try:
            result = await asyncio.wait_for(future, timeout=5.0)
            return result
        except asyncio.TimeoutError:
            logger.error("Buy request timed out")
            return {"error": "timeout"}
    
    async def get_balance(self) -> Dict[str, Any]:
        """Get account balance."""
        req_id = self._get_req_id()
        
        msg = {
            "balance": 1,
            "req_id": req_id
        }
        
        future = asyncio.Future()
        
        def handler(data):
            if not future.done():
                future.set_result(data)
        
        self.message_handlers[req_id] = handler
        
        await self.ws.send(json.dumps(msg))
        
        try:
            result = await asyncio.wait_for(future, timeout=5.0)
            return result
        except asyncio.TimeoutError:
            return {"error": "timeout"}
    
    async def ping(self):
        """Keep connection alive."""
        if self.is_connected and self.ws:
            await self.ws.send(json.dumps({"ping": 1}))
    
    async def disconnect(self):
        """Close WebSocket connection."""
        self.is_connected = False
        
        if self._listen_task:
            self._listen_task.cancel()
            try:
                await self._listen_task
            except asyncio.CancelledError:
                pass
        
        if self.ws:
            await self.ws.close()
            logger.info("🔌 Disconnected from Deriv")
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()