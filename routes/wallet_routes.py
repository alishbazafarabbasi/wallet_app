from flask import Blueprint, request, render_template, redirect, url_for, jsonify, current_app
from utils.keypair_utils import create_keypair_from_secret_key, mnemonic_to_seed, seed_to_keypair
wallet_bp = Blueprint('wallet', __name__)

wallets_db = {}

@wallet_bp.route('/')
def index():
    return render_template('create_wallet.html')

@wallet_bp.route('/create_wallet', methods=['GET', 'POST'])
def create_wallet():
    error = None

    if request.method == 'POST':
        try:
            mnemonic_phrase = request.form.get('mnemonic')

            if not mnemonic_phrase:
                error = "Mnemonic are required."
                raise ValueError(error)

            # Generate seed from mnemonic
            seed = mnemonic_to_seed(mnemonic_phrase)

            # Generate keypair from seed
            keypair = seed_to_keypair(seed)

            public_key = keypair.pubkey()
            private_key_hex = keypair.secret().hex()

            wallet_address = str(public_key)
            mnemonic = str(mnemonic_phrase)
            secret_key = list((keypair.secret()))

            wallets_db[wallet_address] = {
                'public_key': public_key,
                'private_key_hex': private_key_hex,
                'transactions': [],
                'mnemonic_phrase': mnemonic,
                'secret_key': secret_key
            }
            current_app.logger.info(f"Wallet created and stored: {wallet_address}")

            return redirect(url_for('wallet.wallet_details', address=wallet_address))

        except Exception as e:
            current_app.logger.error(f"Error generating wallet: {e}")
            error = 'Failed to generate wallet'

    return render_template('create_wallet.html', error=error)

@wallet_bp.route('/login_wallet', methods=['GET', 'POST'])
def login_wallet():
    error = None

    if request.method == 'POST':
        try:
            secret_key_input = request.form.get('secret_key')
            if not secret_key_input:
                error = 'Secret key is required.'
                raise ValueError(error)

            # Validate and create keypair from the secret key
            keypair = create_keypair_from_secret_key(secret_key_input)
            public_key = keypair.pubkey()
            private_key_hex = keypair.secret().hex()

            wallet_address = str(public_key)

            wallets_db[wallet_address] = {
                'public_key': public_key,
                'private_key_hex': private_key_hex,
                'transactions': [],
                'secret_key': '',
                'mnemonic_phrase': ''
            }

            return redirect(url_for('wallet.wallet_details', address=wallet_address))

        except Exception as e:
            current_app.logger.error(f"Error logging in to wallet: {e}")
            error = 'Failed to login to wallet'

    return render_template('login_wallet.html', error=error)

@wallet_bp.route('/wallet/<address>')
def wallet_details(address):
    if address not in wallets_db:
        current_app.logger.info(f"Wallet not found in database: {address}")
        return jsonify({'error': 'Wallet not found'}), 404

    wallet_info = wallets_db[address]

    return render_template('wallet_details.html',
                           address=address,
                           public_key=wallet_info['public_key'],
                           private_key_hex=wallet_info['private_key_hex'],
                           secret_key= wallet_info['secret_key'],
                           mnemonic_phrase=wallet_info['mnemonic_phrase'])
