from flask import Blueprint, request, render_template, redirect, url_for, jsonify, current_app
from solders.keypair import Keypair
from services.solana_service import solana_client
from utils.keypair_utils import create_keypair_from_secret

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
            wallet_name = request.form.get('wallet_name')
            secret_key_input = request.form.get('secret_key')

            # Validate and create keypair from the secret key
            secret_key = create_keypair_from_secret(secret_key_input)
            if not secret_key:
                error = 'Secret key format is incorrect. Please use comma-separated integers.'
            else:
                keypair = Keypair.from_bytes(secret_key)
                public_key = keypair.pubkey()

                wallet_address = str(public_key)
                wallets_db[wallet_address] = {
                    'wallet_name': wallet_name,
                    'public_key': public_key,
                    'transactions': [],
                }

                return redirect(url_for('wallet.wallet_details', address=wallet_address))

        except Exception as e:
            current_app.logger.error(f"Error generating wallet: {e}")
            error = 'Failed to generate wallet'

    return render_template('create_wallet.html', error=error)


@wallet_bp.route('/wallet/<address>')
def wallet_details(address):
    if address not in wallets_db:
        return jsonify({'error': 'Wallet not found'}), 404

    wallet_info = wallets_db[address]

    return render_template('wallet_details.html',
                           wallet_name=wallet_info['wallet_name'],
                           address=address,
                           public_key=wallet_info['public_key'])