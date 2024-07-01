from flask import Flask, request, jsonify, render_template
from modules.keys import generate_private_key, private_key_to_public_key, public_key_to_address, encrypt_private_key, decrypt_private_key, generate_encryption_key
from modules.transactions import create_transaction, sign_transaction
from modules.qr_code import generate_qr_code
from logging.config import dictConfig
import os
import json

app = Flask(__name__)

# Setup logging
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

# Temporary storage for transactions and keys (for demonstration purposes)
# In a real-world application, use a secure and persistent storage.
transactions_db = {}
keys_db = {}
encryption_key = generate_encryption_key()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_wallet', methods=['POST'])
def generate_wallet():
    try:
        private_key = generate_private_key()
        encrypted_private_key = encrypt_private_key(private_key, encryption_key)
        public_key = private_key_to_public_key(private_key)
        address = public_key_to_address(public_key)

        # Store the encrypted private key and address
        keys_db[address] = {
            'private_key': encrypted_private_key,
            'public_key': public_key
        }

        return jsonify({
            'private_key': encrypted_private_key.hex(),  # Return encrypted private key
            'public_key': public_key.hex(),
            'address': address
        })
    except Exception as e:
        app.logger.error(f"Error generating wallet: {e}")
        return jsonify({'error': 'Failed to generate wallet'}), 500

@app.route('/create_qr', methods=['POST'])
def create_qr():
    try:
        data = request.json.get('data')
        if not data:
            raise ValueError("No data provided for QR code generation")

        qr_code = generate_qr_code(data)
        return jsonify({'qr_code': qr_code})
    except Exception as e:
        app.logger.error(f"Error generating QR code: {e}")
        return jsonify({'error': 'Failed to generate QR code'}), 400

@app.route('/send_transaction', methods=['POST'])
def send_transaction():
    try:
        transaction = request.json.get('transaction')
        private_key_encrypted = request.json.get('private_key')

        if not transaction or not private_key_encrypted:
            raise ValueError("Transaction data or private key missing")

        sender = transaction['sender']
        recipient = transaction['recipient']
        amount = transaction['amount']

        if sender not in keys_db:
            raise ValueError("Invalid sender address")

        # Decrypt the private key
        private_key = decrypt_private_key(bytes.fromhex(private_key_encrypted), encryption_key)
        signature = sign_transaction(transaction, private_key)

        # Store the transaction in the "database"
        transaction_id = len(transactions_db) + 1
        transactions_db[transaction_id] = {
            'transaction': transaction,
            'signature': signature
        }

        return jsonify({'transaction': transaction, 'signature': signature})
    except Exception as e:
        app.logger.error(f"Error signing transaction: {e}")
        return jsonify({'error': 'Failed to sign transaction'}), 400

@app.route('/transaction_history', methods=['POST'])
def transaction_history():
    try:
        address = request.json.get('address')
        if not address:
            raise ValueError("Address not provided")

        # Filter transactions involving the provided address
        relevant_transactions = [
            {
                'transaction_id': tid,
                'sender': tx['transaction']['sender'],
                'recipient': tx['transaction']['recipient'],
                'amount': tx['transaction']['amount']
            }
            for tid, tx in transactions_db.items()
            if tx['transaction']['sender'] == address or tx['transaction']['recipient'] == address
        ]

        return jsonify({'transactions': relevant_transactions})
    except Exception as e:
        app.logger.error(f"Error fetching transaction history: {e}")
        return jsonify({'error': 'Failed to fetch transaction history'}), 400

if __name__ == '__main__':
    app.run(debug=True)
