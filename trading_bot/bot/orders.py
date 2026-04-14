from binance.exceptions import BinanceAPIException, BinanceOrderException
from bot.client import BinanceClient
from bot.logging_config import logger, log_api_interaction

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

    # Structured Request Log
    log_api_interaction("REQUEST", "MARKET_ORDER", payload)

    try:
        response = client.futures_create_order(**payload)
        formatted_res = _format_order_response(response)
        
        # Structured Response Log
        log_api_interaction("RESPONSE", "MARKET_ORDER", formatted_res)
        return formatted_res

    except (BinanceAPIException, BinanceOrderException) as e:
        error_data = {"error": e.message, "code": e.code, "symbol": symbol}
        log_api_interaction("ERROR", "MARKET_ORDER", error_data)
        return {"error": e.message, "code": e.code}
    except Exception as e:
        logger.error(f"Unexpected error placing MARKET order: {str(e)}")
        return {"error": str(e)}

def place_limit_order(symbol: str, side: str, quantity: float, price: float):
    """
    Places a LIMIT order on Binance Futures.
    """
    if client is None:
        logger.error("Binance client not initialized. Cannot place order.")
        return None

    payload = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": "LIMIT",
        "quantity": quantity,
        "price": price,
        "timeInForce": "GTC"
    }

    # Structured Request Log
    log_api_interaction("REQUEST", "LIMIT_ORDER", payload)

    try:
        response = client.futures_create_order(**payload)
        formatted_res = _format_order_response(response)
        
        # Structured Response Log
        log_api_interaction("RESPONSE", "LIMIT_ORDER", formatted_res)
        return formatted_res

    except (BinanceAPIException, BinanceOrderException) as e:
        error_data = {"error": e.message, "code": e.code, "symbol": symbol}
        log_api_interaction("ERROR", "LIMIT_ORDER", error_data)
        return {"error": e.message, "code": e.code}
    except Exception as e:
        logger.error(f"Unexpected error placing LIMIT order: {str(e)}")
        return {"error": str(e)}
