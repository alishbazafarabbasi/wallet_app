from flask import Blueprint, request, render_template, redirect, url_for, jsonify, current_app
from utils.keypair_utils import mnemonic_to_seed, seed_to_keypair, generate_mnemonic

wallet_bp = Blueprint('wallet', __name__)

wallets_db = {}

@wallet_bp.route('/')
def index():
    return render_template('create_wallet.html')

@wallet_bp.route('/create_wallet', methods=['POST'])
def create_wallet():
    try:
        # Choose language based on user preference or default to English
        language = request.form.get('language', 'english')
        mnemonic_phrase = generate_mnemonic(language=language)

        # Generate seed from mnemonic
        seed = mnemonic_to_seed(mnemonic_phrase, language=language)

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

        # Translate mnemonic to Chinese if necessary
        if language == 'chinese_simplified':
            mnemonic_phrase_chinese = mnemonic_phrase
        else:
            mnemonic_phrase_chinese = None

        return render_template('show_mnemonic.html', mnemonic_phrase=mnemonic, mnemonic_phrase_chinese=mnemonic_phrase_chinese)

    except Exception as e:
        current_app.logger.error(f"Error generating wallet: {e}")
        return render_template('create_wallet.html', error='Failed to generate wallet')


@wallet_bp.route('/login_wallet', methods=['POST'])
def login_wallet():
    mnemonic_phrase = request.form.get('mnemonic')
    if not mnemonic_phrase:
        return render_template('show_mnemonic.html', error='Mnemonic phrase is required.')

    try:
        # Generate seed from mnemonic
        seed = mnemonic_to_seed(mnemonic_phrase)

        # Generate keypair from seed
        keypair = seed_to_keypair(seed)

        public_key = keypair.pubkey()
        wallet_address = str(public_key)

        if wallet_address not in wallets_db:
            raise ValueError('Wallet not found.')

        return redirect(url_for('wallet.wallet_details', address=wallet_address))

    except Exception as e:
        current_app.logger.error(f"Error logging in to wallet: {e}")
        return render_template('show_mnemonic.html', error='Failed to login to wallet')


@wallet_bp.route('/login_existing_wallet', methods=['GET', 'POST'])
def login_existing_wallet():
    error = None

    if request.method == 'POST':
        try:
            mnemonic_phrase = request.form.get('mnemonic')
            if not mnemonic_phrase:
                error = 'Mnemonic phrase is required.'
                raise ValueError(error)

            # Generate seed from mnemonic
            seed = mnemonic_to_seed(mnemonic_phrase)

            # Generate keypair from seed
            keypair = seed_to_keypair(seed)

            public_key = keypair.pubkey()

            wallet_address = str(public_key)

            if wallet_address not in wallets_db:
                raise ValueError('Wallet not found.')

            return redirect(url_for('wallet.wallet_details', address=wallet_address))

        except Exception as e:
            current_app.logger.error(f"Error logging in to wallet: {e}")
            error = 'Failed to login to wallet'

    return render_template('login_wallet.html', error=error)
@wallet_bp.route('/wallet/<address>')
def wallet_details(address):
    if address not in wallets_db:
        return jsonify({'error': 'Wallet not found'}), 404

    wallet_info = wallets_db[address]

    return render_template('wallet_details.html',
                           address=address,
                           public_key=wallet_info['public_key'],
                           private_key_hex=wallet_info['private_key_hex'],
                           secret_key=wallet_info['secret_key'],
                           mnemonic_phrase=wallet_info['mnemonic_phrase'])
