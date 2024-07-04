from flask import Flask, request, jsonify, render_template, redirect, url_for
from modules.keys import generate_private_key, private_key_to_public_key, public_key_to_address, encrypt_private_key, decrypt_private_key, generate_encryption_key
from modules.transactions import sign_transaction
from modules.qr_code import generate_qr_code
from logging.config import dictConfig
import os

# Mock balance in SOL and USD
mock_sols = {}
mock_usd = {}

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

# Temporary storage for wallets and transactions (for demonstration purposes)
# In a real-world application, use a secure and persistent storage.
wallets_db = {}
transactions_db = {}
encryption_key = generate_encryption_key()

initial_balance_sol = 100
initial_balance_usd = 29.26
@app.route('/')
def index():
    return render_template('create_wallet.html')

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    try:
        wallet_name = request.form.get('wallet_name')
        mnemonic = request.form.get('mnemonic')
        
        # Generate keys (for demonstration purposes, use random keys)
        private_key = generate_private_key()
        encrypted_private_key = encrypt_private_key(private_key, encryption_key)
        public_key = private_key_to_public_key(private_key)
        address = public_key_to_address(public_key)

        # Store wallet details with initial balance
        wallets_db[address] = {
            'wallet_name': wallet_name,
            'private_key': encrypted_private_key.hex(),
            'public_key': public_key.hex(),
            'transactions': [],  # Initialize empty transactions list
            'balance_sol': mock_sols.get(address, initial_balance_sol),  # Initial SOL balance for new wallet
            'balance_usd': mock_usd.get(address, initial_balance_usd),  # Initial USD balance for new wallet
        }

        # Redirect to wallet details page
        return redirect(url_for('wallet_details', address=address))

    except Exception as e:
        app.logger.error(f"Error generating wallet: {e}")
        return jsonify({'error': 'Failed to generate wallet'}), 500

@app.route('/wallet/<address>')
def wallet_details(address):
    if address not in wallets_db:
        return jsonify({'error': 'Wallet not found'}), 404

    wallet_info = wallets_db[address]

    # Calculate USD balance based on conversion rate (1 USD = 3.8 SOL)
    usd_balance = wallet_info['balance_sol'] / 3.8

    usd_balance_formatted = "{:.2f}".format(usd_balance)
    
    return render_template('wallet_details.html', 
                           wallet_name=wallet_info['wallet_name'], 
                           address=address, 
                           public_key=wallet_info['public_key'], 
                           private_key=wallet_info['private_key'],
                           sol_balance=wallet_info['balance_sol'],
                           usd_balance=usd_balance_formatted)

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

        if sender not in wallets_db:
            raise ValueError("Invalid sender address")

        sender_balance = wallets_db[sender]['balance_sol']

        if sender_balance < amount:
            raise ValueError("Insufficient balance")

        # Deduct from sender's balance
        wallets_db[sender]['balance_sol'] -= amount

        # Decrypt the private key
        private_key = decrypt_private_key(bytes.fromhex(private_key_encrypted), encryption_key)
        signature = sign_transaction(transaction, private_key)

        # Store the transaction in the "database"
        transaction_id = len(transactions_db) + 1
        transactions_db[transaction_id] = {
            'transaction': transaction,
            'signature': signature
        }

        # Update recipient's balance (for demonstration purposes, add amount to balance)
        if recipient in wallets_db:
            wallets_db[recipient]['balance_sol'] += amount
        else:
            # For demonstration, create recipient wallet with initial balance
            wallets_db[recipient] = {
                'wallet_name': f'Wallet for {recipient}',
                'balance_sol': amount,
                'transactions': [],
            }

        # Update sender's transaction list
        wallets_db[sender]['transactions'].append(transaction_id)

        return jsonify({'transaction': transaction, 'signature': signature})

    except Exception as e:
        app.logger.error(f"Error signing transaction: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/transaction_history', methods=['POST'])
def transaction_history():
    address = request.json.get('address')
    if not address:
        return jsonify({'error': 'Address not provided'}), 400

    if address not in wallets_db:
        return jsonify({'error': 'Wallet not found'}), 404

    wallet_transactions = wallets_db[address]['transactions']
    relevant_transactions = [
        {
            'transaction_id': tid,
            'sender': transactions_db[tid]['transaction']['sender'],
            'recipient': transactions_db[tid]['transaction']['recipient'],
            'amount': transactions_db[tid]['transaction']['amount']
        }
        for tid in wallet_transactions
    ]

    return jsonify({'transactions': relevant_transactions})

if __name__ == '__main__':
    app.run(debug=True)
