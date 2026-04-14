# Binance Futures Testnet Trading Bot

A production-quality Python CLI application to place orders on the Binance Futures Testnet.

## Project Overview
This bot allows users to interact with Binance Futures Testnet via a command-line interface. It supports:
- Placing MARKET and LIMIT orders.
- Order validation.
- Robust error handling and logging.

## Features
- **Project Structure**: Modular and scalable.
- **Validation**: Strict input validation before sending to Binance.
- **Logging**: Comprehensive logs stored in `logs/trading.log`.
- **CLI**: Powered by `Typer` for a modern terminal experience.

## Setup Instructions

### 1. Prererequisites
- Python 3.8+
- Binance Testnet API Credentials

### 2. Environment Setup
1. Clone the repository and navigate to the project folder.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Update the `.env` file with your Binance Testnet API Key and Secret:
```env
API_KEY=your_key
API_SECRET=your_secret
BASE_URL=https://testnet.binancefuture.com
```

### 5. Running the Bot
```bash
python -m bot.cli --help
```

## Directory Structure
- `bot/`: Core application logic.
- `logs/`: Application logs.
- `.env`: Environment variables (secret).
- `requirements.txt`: Dependencies.
