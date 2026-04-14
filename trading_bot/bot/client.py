import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
from bot.logging_config import logger, log_api_interaction

# Load environment variables from .env file
load_dotenv()

class BinanceClient:
    """
    A reusable client for interacting with the Binance Futures Testnet.
    """

    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        self.base_url = os.getenv("BASE_URL", "https://testnet.binancefuture.com")
        self.client = None

        if not self.api_key or not self.api_secret:
            logger.error("API_KEY or API_SECRET not found in environment variables.")
            raise ValueError("API_KEY and API_SECRET must be provided in .env file.")

    def get_client(self):
        """
        Initializes and returns the Binance client for Futures.
        """
        if self.client is None:
            try:
                # Initialize the client specifically for testnet if configured
                self.client = Client(self.api_key, self.api_secret, testnet=True)
                # Ensure the client is pointing to the correct futures URL if needed, 
                # python-binance handles this via testnet=True for most endpoints.
                logger.info("Binance client initialized for testnet.")
            except Exception as e:
                logger.error(f"Failed to initialize Binance client: {str(e)}")
                raise
        return self.client

    def test_connection(self):
        """
        Tests the connection to the Binance Futures API by fetching account information.
        Returns:
            bool: True if connection is successful, False otherwise.
        """
        client = self.get_client()
        log_api_interaction("REQUEST", "ACCOUNT_INFO", {"test": True})
        try:
            # Fetch futures account info to verify connectivity and credentials
            account_info = client.futures_account()
            log_api_interaction("RESPONSE", "ACCOUNT_INFO", {"status": "success", "canDeposit": account_info.get('canDeposit')})
            logger.info("Successfully connected to Binance Futures Testnet.")
            return True
        except BinanceAPIException as e:
            error_data = {"error": e.message, "code": e.code}
            log_api_interaction("ERROR", "ACCOUNT_INFO", error_data)
        except Exception as e:
            logger.error(f"Unexpected error during connection test: {str(e)}")
        
        return False

# Singleton-like access if needed, though class instantiation is fine
if __name__ == "__main__":
    # Quick test if run directly
    try:
        trading_client = BinanceClient()
        if trading_client.test_connection():
            print("Connection successful!")
        else:
            print("Connection failed.")
    except Exception as err:
        print(f"Error: {err}")
