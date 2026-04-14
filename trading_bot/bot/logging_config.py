import logging
import os
from pathlib import Path

def setup_logging():
    """Sets up logging configuration for the trading bot."""
    log_dir = Path(__file__).parent.parent / "logs"
    log_file = log_dir / "trading.log"

    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also log to console for CLI visibility
        ]
    )

    logger = logging.getLogger("trading_bot")
    logger.info("Logging initialized.")
    return logger

# Initialize logging when module is imported
logger = setup_logging()
