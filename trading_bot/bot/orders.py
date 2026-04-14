from binance.exceptions import BinanceAPIException, BinanceOrderException
from bot.client import BinanceClient
from bot.logging_config import logger

# Initialize the Binance client
try:
    binance_manager = BinanceClient()
    client = binance_manager.get_client()
except Exception as e:
    logger.critical(f"Could not initialize Binance client in orders module: {e}")
    client = None

def _format_order_response(response):
    """
    Extracts and formats key information from the Binance order response.
    """
    return {
        "orderId": response.get("orderId"),
        "status": response.get("status"),
        "executedQty": response.get("executedQty"),
        "avgPrice": response.get("avgPrice") or response.get("price", "0.0"),
        "symbol": response.get("symbol"),
        "side": response.get("side"),
        "type": response.get("type")
    }

def place_market_order(symbol: str, side: str, quantity: float):
    """
    Places a MARKET order on Binance Futures.
    
    Args:
        symbol (str): Trading pair (e.g., 'BTCUSDT')
        side (str): 'BUY' or 'SELL'
        quantity (float): Amount to trade
    """
    if client is None:
        logger.error("Binance client not initialized. Cannot place order.")
        return None

    payload = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": "MARKET",
        "quantity": quantity
    }

    logger.info(f"Placing MARKET order: {payload}")

    try:
        response = client.futures_create_order(**payload)
        formatted_res = _format_order_response(response)
        logger.info(f"MARKET order successful: {formatted_res}")
        return formatted_res

    except (BinanceAPIException, BinanceOrderException) as e:
        logger.error(f"Binance API Error placing MARKET order: {e.message} (Code: {e.code})")
        return {"error": e.message, "code": e.code}
    except Exception as e:
        logger.error(f"Unexpected error placing MARKET order: {str(e)}")
        return {"error": str(e)}

def place_limit_order(symbol: str, side: str, quantity: float, price: float):
    """
    Places a LIMIT order on Binance Futures.
    
    Args:
        symbol (str): Trading pair (e.g., 'BTCUSDT')
        side (str): 'BUY' or 'SELL'
        quantity (float): Amount to trade
        price (float): Limit price
    """
    if client is None:
        logger.error("Binance client not initialized. Cannot place order.")
        return None

    # Common policy for LIMIT orders: Good Till Cancel (GTC)
    payload = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": "LIMIT",
        "quantity": quantity,
        "price": price,
        "timeInForce": "GTC"
    }

    logger.info(f"Placing LIMIT order: {payload}")

    try:
        response = client.futures_create_order(**payload)
        formatted_res = _format_order_response(response)
        logger.info(f"LIMIT order successful: {formatted_res}")
        return formatted_res

    except (BinanceAPIException, BinanceOrderException) as e:
        logger.error(f"Binance API Error placing LIMIT order: {e.message} (Code: {e.code})")
        return {"error": e.message, "code": e.code}
    except Exception as e:
        logger.error(f"Unexpected error placing LIMIT order: {str(e)}")
        return {"error": str(e)}
