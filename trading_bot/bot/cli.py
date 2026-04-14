import typer
from typing import Optional
from bot.orders import place_market_order, place_limit_order
from bot.validators import validate_inputs
from bot.logging_config import logger
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Binance Futures Testnet Trading Bot CLI")
console = Console()

@app.command()
def place_order(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading symbol (e.g., BTCUSDT)"),
    side: str = typer.Option(..., "--side", "-d", help="Order side (BUY or SELL)"),
    order_type: str = typer.Option(..., "--type", "-t", help="Order type (MARKET or LIMIT)"),
    quantity: float = typer.Option(..., "--quantity", "-q", help="Quantity to trade"),
    price: Optional[float] = typer.Option(None, "--price", "-p", help="Price (required for LIMIT orders)")
):
    """
    Validates and executes an order on Binance Futures Testnet.
    """
    logger.info(f"CLI command received: {side} {order_type} {quantity} {symbol} @ {price}")

    try:
        # Step 1: Validate Inputs
        valid_data = validate_inputs(symbol, side, order_type, quantity, price)
        
        console.print(f"\n[bold blue]Order Summary:[/bold blue]")
        console.print(f"Symbol: {valid_data['symbol']}")
        console.print(f"Side: {valid_data['side']}")
        console.print(f"Type: {valid_data['type']}")
        console.print(f"Quantity: {valid_data['quantity']}")
        if valid_data['type'] == "LIMIT":
            console.print(f"Price: {valid_data['price']}")

        confirm = typer.confirm("\nAre you sure you want to place this order?")
        if not confirm:
            console.print("[yellow]Order cancelled by user.[/yellow]")
            return

        # Step 2: Execute Order
        console.print("\n[yellow]Executing order...[/yellow]")
        
        if valid_data['type'] == "MARKET":
            response = place_market_order(
                valid_data['symbol'], 
                valid_data['side'], 
                valid_data['quantity']
            )
        else:
            response = place_limit_order(
                valid_data['symbol'], 
                valid_data['side'], 
                valid_data['quantity'], 
                valid_data['price']
            )

        # Step 3: Display Response
        if response and "error" not in response:
            console.print("\n[bold green]✔ Success! Order Placed.[/bold green]")
            
            table = Table(title="Binance Response")
            table.add_column("Key", style="cyan")
            table.add_column("Value", style="magenta")
            
            for key, val in response.items():
                table.add_row(key, str(val))
            
            console.print(table)
        else:
            error_msg = response.get("error", "Unknown error") if response else "Connection failed"
            console.print(f"\n[bold red]✘ Failure: {error_msg}[/bold red]")
            logger.error(f"Order failed: {error_msg}")

    except ValueError as val_err:
        console.print(f"\n[bold red]Validation Error:[/bold red] {str(val_err)}")
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        logger.exception("An unexpected error occurred in the CLI.")

if __name__ == "__main__":
    app()
