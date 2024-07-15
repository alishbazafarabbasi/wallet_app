import unittest
from unittest.mock import patch
from flask import Flask, json
from routes.transaction_routes import transaction_bp
from services.solana_service import solana_client, transfer_sol_service, get_balance_in_sol
class TransactionBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(transaction_bp)
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

        # Mocking wallets_db within the app context
        self.app.config['wallets_db'] = {   
            'test_address': {
                'transactions': ['tx1', 'tx2']
            },
            'tx1': {
                'transaction': {
                    'sender': 'sender_address_1',
                    'recipient': 'recipient_address_1',
                    'amount': 1.23
                }
            },
            'tx2': {
                'transaction': {
                    'sender': 'sender_address_2',
                    'recipient': 'recipient_address_2',
                    'amount': 4.56
                }
            }
        }

    @patch('services.solana_service.solana_client.get_balance')
    def test_get_wallet_balance(self, mock_get_balance):

        # Mock the balance response
        mock_get_balance.return_value.value = 5000000000
        print("mock_get_balancemock_get_balance",mock_get_balance)

        # Make a POST request to the endpoint
        response = self.client.post('/get_wallet_balance', json={'address': '9rF3Pb8cXU2sBPkrrbuFftWCu6qzTDvJABgaYrdUBPDw'})

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Parse the response JSON data
        data = response.get_json()
        balance = data['balance']
        status = data['status']
        # Assert the expected values
        self.assertEqual(status, 'success')
        self.assertEqual(balance, 5)
    @patch('services.solana_service.transfer_sol_service')
    def test_transfer_sol(self, mock_transfer_sol):
        mock_transfer_sol.return_value = {
            'status': 'Success',
            'tx_id': 'dummy_tx_id'
        }  # Mock the transfer response
        response = self.client.post('/transfer_sol', json={
            'sender_address': 'sender_address',
            'receiver_address': 'receiver_address',
            'amount': 1.23,
            'private_key': 'private_key'
        })
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'Success')  # Make sure to match the case correctly

if __name__ == '__main__':
    unittest.main()