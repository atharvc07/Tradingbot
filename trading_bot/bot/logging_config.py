import logging
import os
import json
from pathlib import Path
from datetime import datetime

class StructuredFormatter(logging.Formatter):
    """
    A custom formatter that ensures logs are structured and highly readable.
    """
    def format(self, record):
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S'),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage()
        }
        
        # If there's extra data passed via 'extra', we could include it here.
        # But for CLI readability, we'll format it as a clean string.
        return f"{log_data['timestamp']} | {log_data['level']:8} | {log_data['module']:12} | {log_data['message']}"

def setup_logging():
    """Sets up an enhanced logging configuration for the trading bot."""
    log_dir = Path(__file__).parent.parent / "logs"
    log_file = log_dir / "trading.log"

    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Base logger
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if setup_logging is called multiple times
    if not logger.handlers:
        # File Handler (Full detail)
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(module)s:%(funcName)s:%(lineno)d | %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        
        # Console Handler (Clean/Readable for user)
        console_handler = logging.StreamHandler()
        console_formatter = StructuredFormatter()
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Initialize logger
logger = setup_logging()

def log_api_interaction(direction: str, payload_type: str, data: dict):
    """
    Helper to log API requests and responses in a structured key-value format.
    
    Args:
        direction (str): 'REQUEST' or 'RESPONSE'
        payload_type (str): Type of interaction (e.g., 'MARKET_ORDER')
        data (dict): The actual data to log
    """
    # Filter out sensitive keys from logs if present
    sanitized_data = {k: v for k, v in data.items() if k not in ["api_key", "api_secret"]}
    
    # Format: REQUEST | TYPE | {key: val, ...}
    msg = f"{direction:8} | {payload_type:15} | {json.dumps(sanitized_data)}"
    logger.info(msg)
