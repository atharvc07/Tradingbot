Binance Futures Testnet Trading Bot (Python CLI)
A professional-grade CLI application for executing orders on the Binance Futures Testnet. Built with a modular architecture, robust validation, and structured logging.

🚀 Features
Production-Quality Structure: Clean separation of concerns (Logic, Validation, Client, CLI).
Modern CLI: Intuitive interface powered by Typer and Rich.
Structured Logging: Automatic API request/response logging with sensitive data filtering.
Strict Validation: Pre-flight checks for symbols, quantities, and order types to prevent API waste.
Fail-Safe Mode: Confirmation prompts before order execution.
🛠️ Project Structure
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API connection & auth
│   ├── orders.py          # MARKET and LIMIT order execution logic
│   ├── validators.py      # Strict input validation logic
│   ├── logging_config.py  # Structured logging & API interaction tracking
│   └── cli.py             # CLI entry point and user interaction
├── logs/
│   └── trading.log        # Rolling logs for auditing
├── .env                   # API Credentials (ignored by git)
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
⚙️ Setup Instructions
1. Pre-requisites
Python 3.8+
Binance Futures Testnet Account (Generates API Keys)
2. Installation
Clone the repository.
Initialize and activate a virtual environment:
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
Install dependencies:
pip install -r requirements.txt
3. Configuration
Rename the .env template or create a new one with your keys:

API_KEY=your_testnet_api_key
API_SECRET=your_testnet_api_secret
BASE_URL=https://testnet.binancefuture.com
💻 Usage Examples
The tool is invoked as a Python module:

Place a MARKET Buy Order
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
Place a LIMIT Sell Order
python -m bot.cli -s ETHUSDT -d SELL -t LIMIT -q 0.1 -p 3200.50
Get Help
python -m bot.cli --help
🛡️ Error Handling
The bot handles common trading errors gracefully:

Insufficient Margin: Returns a clear message if your testnet balance is too low.
Invalid Symbol: Automatically formats input (e.g., ethusdt -> ETHUSDT) and validates pair existence.
Network Issues: Retries and clear exception logging via python-binance.
📝 Logging
Detailed logs are stored in logs/trading.log.

Request: Logs the payload sent to Binance.
Response: Logs the unique orderId and fill status.
Safety: API Secrets are never written to log files.
