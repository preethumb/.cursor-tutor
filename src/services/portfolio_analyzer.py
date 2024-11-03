from datetime import datetime
import pandas as pd

class PortfolioAnalyzer:
    def __init__(self, db_session):
        self.session = db_session
    
    def get_total_portfolio_value(self, as_of_date=None):
        if not as_of_date:
            as_of_date = datetime.utcnow()
            
        positions = self.session.query(Position).all()
        total_value = sum(p.quantity * p.current_price for p in positions)
        cash_balance = self.get_cash_balance(as_of_date)
        return total_value + cash_balance
    
    def get_returns(self, start_date, end_date):
        """Calculate returns between two dates, including:
        - Price appreciation
        - Dividends
        - Interest earned
        - Adjusted for deposits/withdrawals
        """
        starting_value = self._get_portfolio_value_at_date(start_date)
        ending_value = self._get_portfolio_value_at_date(end_date)
        
        # Get all cash flows between dates
        cash_flows = self._get_cash_flows_between_dates(start_date, end_date)
        
        # Calculate time-weighted return
        return self._calculate_time_weighted_return(
            starting_value, 
            ending_value, 
            cash_flows
        )
    
    def get_holdings_by_account(self):
        """Returns a breakdown of holdings across all accounts"""
        accounts = self.session.query(Account).all()
        holdings = {}
        
        for account in accounts:
            holdings[account.name] = {
                'cash': self.get_cash_balance(account_id=account.id),
                'positions': [
                    {
                        'symbol': p.symbol,
                        'quantity': p.quantity,
                        'market_value': p.quantity * p.current_price,
                        'cost_basis': p.cost_basis
                    }
                    for p in account.positions
                ]
            }
        
        return holdings 