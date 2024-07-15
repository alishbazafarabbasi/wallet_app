from flask import Blueprint, request, jsonify, current_app
from services.solana_service import solana_client, transfer_sol_service, get_balance_in_sol

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/get_wallet_balance', methods=['POST'])
def get_wallet_balance():
    try:
        data = request.get_json()
        address = data.get('address')

        if not address:
            return jsonify({'status': 'error', 'message': 'Address not provided'}), 400

        balance_sol = get_balance_in_sol(address)
        return jsonify({'status': 'success', 'balance': balance_sol}), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching wallet balance: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@transaction_bp.route('/transfer_sol', methods=['POST'])
def transfer_sol():
    try:
        data = request.json
        sender_address = data.get('sender_address')
        receiver_address = data.get('receiver_address')
        amount = data.get('amount')
        sender_private_key = data.get('private_key')

        print(f"sender_address: {sender_address}, receiver_address: {receiver_address}, amount: {amount}, private_key: {sender_private_key}")

        if not sender_address or not amount or not sender_private_key:
            return jsonify({'error': 'Invalid transaction data'}), 400

        response_data = transfer_sol_service(sender_address, receiver_address, amount, sender_private_key)
        return jsonify(response_data), 200

    except Exception as e:
        current_app.logger.error(f"Error transferring SOL: {e}")
        return jsonify({'error': f"Error transferring SOL:{e}"}),500