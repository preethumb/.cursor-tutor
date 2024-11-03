import click
from datetime import datetime
from ..services.data_import import DataImportService

@click.group()
def cli():
    """Portfolio Management CLI"""
    pass

@cli.command()
@click.argument('file_path')
@click.option('--type', type=click.Choice(['transactions', 'positions', 'accounts']), required=True)
def import_csv(file_path: str, type: str):
    """Import data from CSV file"""
    service = DataImportService(db_session)  # You'll need to set up db_session
    results = service.process_csv(file_path, type)
    click.echo(f"Processed {results['total']} rows")
    click.echo(f"Successful imports: {results['success']}")
    if results['errors']:
        click.echo("\nErrors:")
        for error in results['errors']:
            click.echo(f"- {error}")

@cli.command()
@click.option('--account', required=True, help='Account name or ID')
@click.option('--type', required=True, 
              type=click.Choice(['BUY', 'SELL', 'DIVIDEND', 'DEPOSIT', 'WITHDRAWAL']))
@click.option('--symbol', help='Stock symbol (required for BUY/SELL)')
@click.option('--quantity', type=float, help='Quantity (required for BUY/SELL)')
@click.option('--price', type=float, help='Price per share (required for BUY/SELL)')
@click.option('--amount', type=float, help='Total amount (required for DEPOSIT/WITHDRAWAL)')
@click.option('--date', default=str(datetime.now().date()), 
              help='Transaction date (YYYY-MM-DD)')
def add_transaction(account, type, symbol, quantity, price, amount, date):
    """Add a single transaction via command line"""
    service = DataImportService(db_session)
    
    # Validate inputs based on transaction type
    if type in ['BUY', 'SELL'] and not all([symbol, quantity, price]):
        raise click.BadParameter("Symbol, quantity, and price are required for BUY/SELL transactions")
    
    if type in ['DEPOSIT', 'WITHDRAWAL'] and not amount:
        raise click.BadParameter("Amount is required for DEPOSIT/WITHDRAWAL transactions")
    
    # Create transaction data
    transaction_data = {
        'account': account,
        'type': type,
        'symbol': symbol,
        'quantity': quantity,
        'price': price,
        'total_amount': amount or (quantity * price),
        'date': datetime.strptime(date, '%Y-%m-%d')
    }
    
    try:
        service._process_transaction_row(transaction_data)
        service.session.commit()
        click.echo("Transaction added successfully!")
    except Exception as e:
        click.echo(f"Error adding transaction: {str(e)}", err=True) 