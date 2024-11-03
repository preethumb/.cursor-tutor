import csv
from datetime import datetime
import click
from typing import Optional, Dict, Any

class DataImportService:
    def __init__(self, db_session):
        self.session = db_session
        
    def process_csv(self, file_path: str, import_type: str) -> Dict[str, Any]:
        """
        Process CSV files for different types of data imports
        import_type can be: 'transactions', 'positions', 'accounts'
        """
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                
                # Validate headers
                self._validate_headers(reader.fieldnames, import_type)
                
                results = {
                    'success': 0,
                    'errors': [],
                    'total': 0
                }
                
                for row in reader:
                    try:
                        if import_type == 'transactions':
                            self._process_transaction_row(row)
                        elif import_type == 'positions':
                            self._process_position_row(row)
                        elif import_type == 'accounts':
                            self._process_account_row(row)
                        
                        results['success'] += 1
                    except Exception as e:
                        results['errors'].append(f"Row {results['total'] + 1}: {str(e)}")
                    
                    results['total'] += 1
                
                self.session.commit()
                return results
                
        except Exception as e:
            raise Exception(f"Error processing CSV: {str(e)}")
    
    def _validate_headers(self, headers: list, import_type: str) -> None:
        required_headers = {
            'transactions': ['date', 'account', 'type', 'symbol', 'quantity', 'price', 'total_amount'],
            'positions': ['account', 'symbol', 'quantity', 'cost_basis'],
            'accounts': ['name', 'account_type', 'institution']
        }
        
        missing = set(required_headers[import_type]) - set(headers)
        if missing:
            raise ValueError(f"Missing required headers: {missing}") 