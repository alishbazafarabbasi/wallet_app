import unittest
from app import generate_wallet, send_transaction

class TestBlockchainWallet(unittest.TestCase):
    def test_generate_wallet(self):
        wallet = generate_wallet()
        self.assertIn('address', wallet)
        self.assertIn('private_key', wallet)
        self.assertIn('public_key', wallet)

    def test_send_transaction(self):
        response = send_transaction('sender_address', 'recipient_address', 10)
        self.assertEqual(response.status_code, 200)
        self.assertIn('transaction_id', response.json())

if __name__ == '__main__':
    unittest.main()
