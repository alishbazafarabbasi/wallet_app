import unittest
import json
from flask import url_for
from app import app, wallets_db, transactions_db, encryption_key
from modules.keys import generate_private_key, private_key_to_public_key, public_key_to_address, encrypt_private_key, decrypt_private_key

class BlockchainWalletTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Generate test wallet
        self.wallet_name = "Test Wallet"
        self.private_key = generate_private_key()
        self.encrypted_private_key = encrypt_private_key(self.private_key, encryption_key).hex()
        self.public_key = private_key_to_public_key(self.private_key).hex()
        self.address = public_key_to_address(self.public_key)
        self.initial_balance_sol = 100

        # Add test wallet to the wallets_db
        wallets_db[self.address] = {
            'wallet_name': self.wallet_name,
            'private_key': self.encrypted_private_key,
            'public_key': self.public_key,
            'transactions': [],
            'balance_sol': self.initial_balance_sol,
            'balance_usd': self.initial_balance_sol / 3.8
        }

    def test_create_wallet(self):
        response = self.app.post('/create_wallet', data=dict(wallet_name="New Wallet", mnemonic="test mnemonic"))
        self.assertEqual(response.status_code, 302)  # Redirect to wallet details page

    def test_wallet_details(self):
        response = self.app.get(f'/wallet/{self.address}')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode('utf-8')
        self.assertIn(self.wallet_name, data)
        self.assertIn(self.address, data)
        self.assertIn(str(self.initial_balance_sol), data)

    def test_send_transaction_insufficient_balance(self):
        transaction = {
            'sender': self.address,
            'recipient': 'recipient_address',
            'amount': self.initial_balance_sol + 1  # Exceeds balance
        }
        response = self.app.post('/send_transaction', 
                                 data=json.dumps({'transaction': transaction, 'private_key': self.encrypted_private_key}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('Insufficient balance', data['error'])

    def test_send_transaction_success(self):
        recipient_address = 'recipient_address'
        amount = 10
        transaction = {
            'sender': self.address,
            'recipient': recipient_address,
            'amount': amount
        }
        response = self.app.post('/send_transaction',
                                 data=json.dumps({'transaction': transaction, 'private_key': self.encrypted_private_key}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('signature', data)
        self.assertEqual(wallets_db[self.address]['balance_sol'], self.initial_balance_sol - amount)
        self.assertEqual(wallets_db[recipient_address]['balance_sol'], amount)

    def test_transaction_history(self):
        # Send a transaction to create a transaction history
        recipient_address = 'recipient_address'
        amount = 10
        transaction = {
            'sender': self.address,
            'recipient': recipient_address,
            'amount': amount
        }
        self.app.post('/send_transaction',
                      data=json.dumps({'transaction': transaction, 'private_key': self.encrypted_private_key}),
                      content_type='application/json')

        response = self.app.post('/transaction_history',
                                 data=json.dumps({'address': self.address}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('transactions', data)
        self.assertEqual(len(data['transactions']), 1)
        self.assertEqual(data['transactions'][0]['amount'], amount)
        self.assertEqual(data['transactions'][0]['sender'], self.address)
        self.assertEqual(data['transactions'][0]['recipient'], recipient_address)

if __name__ == '__main__':
    unittest.main()
