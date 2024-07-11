from flask import Flask, request, jsonify, render_template, redirect, url_for
from solana.rpc.api import Client
from solders.keypair import Keypair 
import requests
import logging
from solders.transaction import VersionedTransaction
from solders.system_program import transfer, TransferParams
from solders.message import MessageV0



app = Flask(__name__)
app.logger.setLevel(logging.INFO) 

wallets_db = {}

logging.basicConfig(level=logging.DEBUG)

# Replace with your actual Solana RPC URL
solana_rpc_url = "https://api.devnet.solana.com"
solana_client = Client(solana_rpc_url)

@app.route('/')
def index():
    return render_template('create_wallet.html')

@app.route('/create_wallet', methods=['GET', 'POST'])
def create_wallet():
    error = None

    if request.method == 'POST':
        try:
            wallet_name = request.form.get('wallet_name')
            secret_key_input = request.form.get('secret_key')
            
            # Validate secret_key format (comma-separated integers)
            try:
                secret_key = list(map(int, secret_key_input.split(',')))
            except ValueError:
                error = 'Secret key format is incorrect. Please use comma-separated integers.'

            if not error:
                # Create keypair from the secret key
                keypair = Keypair.from_bytes(secret_key)
                print(f"Created Keypair with public key: {keypair.pubkey()}")

                public_key = keypair.pubkey()

                # Store wallet details
                wallet_address = str(public_key)
                wallets_db[wallet_address] = {
                    'wallet_name': wallet_name,
                    'public_key': public_key,
                    'transactions': [],
                }

                # Redirect to wallet details page
                return redirect(url_for('wallet_details', address=wallet_address))

        except Exception as e:
            app.logger.error(f"Error generating wallet: {e}")
            error = 'Failed to generate wallet'

    # Render the template with or without error message
    return render_template('create_wallet.html',error=error)
                           
@app.route('/wallet/<address>')
def wallet_details(address):
    if address not in wallets_db:
        return jsonify({'error': 'Wallet not found'}), 404

    wallet_info = wallets_db[address]

    return render_template('wallet_details.html',
                           wallet_name=wallet_info['wallet_name'],
                           address=address,
                           public_key=wallet_info['public_key'])

@app.route('/transaction_history', methods=['POST'])
def transaction_history():
    try:
        data = request.json
        address = data.get('address')

        if not address:
            return jsonify({'error': 'Address not provided'}), 400

        if address not in wallets_db:
            return jsonify({'error': 'Wallet not found'}), 404

        wallet_transactions = wallets_db[address]['transactions']
        relevant_transactions = [
            {
                'transaction_id': tid,
                'sender': wallets_db[tid]['transaction']['sender'],
                'recipient': wallets_db[tid]['transaction']['recipient'],
                'amount': wallets_db[tid]['transaction']['amount']
            }
            for tid in wallet_transactions
        ]

        return jsonify({'transactions': relevant_transactions})

    except Exception as e:
        app.logger.error(f"Error fetching transaction history: {e}")
        return jsonify({'error': f"Error fetching transaction history: {e}"}), 500

@app.route('/faucet', methods=['POST'])
def faucet():
    print("Faucet request received", request.headers['Content-Type'])
    if request.headers['Content-Type'] != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.json
    wallet_address = data.get('wallet_address')

    if not wallet_address:
        return jsonify({'error': 'Wallet address not provided'}), 400

    # Example of interacting with Solana faucet API directly
    faucet_url = "https://faucet.solana.com/"
    faucet_params = {"address": wallet_address}

    try:
        response = requests.post(faucet_url, json=faucet_params)
        response_data = response.json()  # Attempt to parse response JSON

        print(f"Response: {response_data}")

        if response.status_code == 200:
            # Update balance in wallets_db (for demonstration purposes)
            if wallet_address in wallets_db:
                wallets_db[wallet_address]['balance_sol'] += 10  # Assuming faucet sends 10 SOL

            return jsonify({"message": "Airdrop request successful!"})
        else:
            return jsonify({"error": f"Airdrop request failed: {response.status_code}, {response_data}"}), 500

    except Exception as e:
        return jsonify({"error": f"Exception during faucet request: {str(e)}"}), 500

@app.route('/get_wallet_balance', methods=['POST'])
def get_wallet_balance():
    try:
        receiver_keypair = Keypair()

        data = request.get_json()
        address = data.get('address')
        a_public_key = receiver_keypair.pubkey().from_string(address)

        # Check the balance
        if not address:
            return jsonify({'status': 'error', 'message': 'Address not provided'}), 400

        # Retrieve balance using Solana RPC
        balance_response = solana_client.get_balance(a_public_key)

        print("balance_response: ", type(balance_response))

        # Assuming GetBalanceResp has a method or attribute to access the balance
        balance_value = balance_response.value
        print("balance_value: ", balance_value)

        balance_sol = 0

        if balance_value > 0:
            balance_sol = balance_value / 1000000000

        return jsonify({'status': 'success', 'balance': balance_sol}), 200
    except Exception as e:
        app.logger.error(f"Error fetching wallet balance: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
def dapp_interaction_instruction(sender_pubkey, amount):
    # Replace this with actual DApp interaction logic
    return transfer(
        TransferParams(
            from_pubkey=sender_pubkey,
            to_pubkey=sender_pubkey,  # self-transfer
            lamports=amount
        )
    )


@app.route('/transfer_sol', methods=['POST'])
def transfer_sol():
    try:
        # Get data from request
        sender_address = request.json.get('sender_address')
        receiver_address = request.json.get('receiver_address')
        amount = request.json.get('amount')
        sender_private_key = request.json.get('private_key')


        # Validate the input
        if not sender_address or not amount or not sender_private_key:
            return jsonify({'error': 'Invalid transaction data'}), 400

        # Decode the sender's private key
        sender_keypair = Keypair()
        receiver_ad = Keypair()
        sender_pub_key_ = sender_keypair.pubkey()


        if receiver_address:
            # Create transfer instruction
            receiver_public_key = receiver_ad.pubkey()
            amount = int(amount)  # Amount in lamports (1 SOL = 1,000,000,000 lamports)

            ix = transfer(
                TransferParams(
                    from_pubkey=sender_pub_key_,
                    to_pubkey=receiver_public_key,
                    lamports=amount
                )
            )
        else:
            # Example: Interact with a DApp
            ix = dapp_interaction_instruction(sender_pub_key_, amount)

        # Get recent blockhash
        blockhash_response = solana_client.get_latest_blockhash()
        print("blockhash_response: ", blockhash_response)

        if blockhash_response.value:
            blockhash = blockhash_response.value.blockhash   
        else:
            raise Exception("Failed to fetch the latest blockhash")
        
        
        print("blockhash: ", blockhash)

        # Create message
        msg = MessageV0.try_compile(
            payer=sender_pub_key_,
            instructions=[ix],
            address_lookup_table_accounts=[],
            recent_blockhash=blockhash,
        )
        print("msg: ", msg)

        # Create transaction
        tx = VersionedTransaction(msg, [sender_keypair])
        
        
        print("tx: ", tx)

        recent_blockhash = tx.message.recent_blockhash
        str_hash = str(recent_blockhash)


        signature = tx.signatures[0]
        str_signature = str(signature)
        print(" tx.signatures[0]: ",  str_signature)

        response_data = {
            'recent_blockhash': str_hash,
            'status': 'Success',
            'tx_id': str_signature
        }

        print("response_data: ", response_data)

        # transaction_url = f"https://explorer.solana.com/tx/{tx_id}?cluster=devnet"
        # print("transaction_url: ", transaction_url)
        return jsonify(response_data), 200

    except Exception as e:
        app.logger.error(f"Error transferring SOL: {e}")
        return jsonify({'error': f"Error transferring SOL: {e}"}), 500

# Setup logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__': 
    app.run(debug=True)
