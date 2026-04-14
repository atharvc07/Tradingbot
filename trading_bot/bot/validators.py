from bot.logging_config import logger

def validate_symbol(symbol: str) -> str:
    """Validates and formats the trading symbol."""
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string.")
    return symbol.upper().strip()

def validate_side(side: str) -> str:
    """Validates the order side."""
    side = side.upper().strip()
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be either 'BUY' or 'SELL'.")
    return side

def validate_order_type(order_type: str) -> str:
    """Validates the order type."""
    order_type = order_type.upper().strip()
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError("Order type must be either 'MARKET' or 'LIMIT'.")
    return order_type

def validate_quantity(quantity: float) -> float:
    """Validates that quantity is a positive number."""
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")
    return float(quantity)

def validate_price(price: float, order_type: str) -> float:
    """Validates price for LIMIT orders."""
    if order_type == "LIMIT":
        if price is None or price <= 0:
            raise ValueError("Price must be greater than zero for LIMIT orders.")
    return float(price) if price else 0.0

def validate_inputs(symbol, side, order_type, quantity, price=None):
    """
    Consolidated validation for all order inputs.
    """
    try:
        validated_symbol = validate_symbol(symbol)
        validated_side = validate_side(side)
        validated_type = validate_order_type(order_type)
        validated_qty = validate_quantity(quantity)
        validated_price = validate_price(price, validated_type)

        return {
            "symbol": validated_symbol,
            "side": validated_side,
            "type": validated_type,
            "quantity": validated_qty,
            "price": validated_price
        }
    except ValueError as e:
        logger.error(f"Input validation failed: {str(e)}")
        raise
