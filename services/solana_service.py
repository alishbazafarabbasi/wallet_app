from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.system_program import transfer, TransferParams
from solders.message import MessageV0
from solders.transaction import VersionedTransaction
from config import Config

solana_client = Client(Config.SOLANA_RPC_URL)


def get_balance_in_sol(address):
    public_key = Keypair().pubkey().from_string(address)
    balance_response = solana_client.get_balance(public_key)
    balance_value = balance_response.value
    if balance_value is None:
        return 0
    if balance_value > 0:
        return balance_value / 1000000000

def transfer_sol_service(sender_address, receiver_address, amount, sender_private_key):
    print(f"sender_address: {sender_address}, receiver_address: {receiver_address}, amount: {amount}, private_key: {sender_private_key}")
    try:
        sender_keypair = Keypair()
    except ValueError:
        return {'error': 'Invalid private key format. Private key should be a comma-separated list of integers.'}
    
    receiver_keypair = Keypair()

    ix = transfer(
        TransferParams(
            from_pubkey=sender_keypair.pubkey(),
            to_pubkey=receiver_keypair.pubkey(),
            lamports=int(amount)
        )
    )

    blockhash_response = solana_client.get_latest_blockhash()
    if blockhash_response is None:
        return {'error': 'Failed to get latest blockhash'}
    
    if blockhash_response.value.blockhash is None:
        return {'error': 'Failed to get latest blockhash'}
    
    blockhash = blockhash_response.value.blockhash

    msg = MessageV0.try_compile(
        payer=sender_keypair.pubkey(),
        instructions=[ix],
        address_lookup_table_accounts=[],
        recent_blockhash=blockhash,
    )

    tx = VersionedTransaction(msg, [sender_keypair])

    return {
        'recent_blockhash': str(tx.message.recent_blockhash),
        'status': 'Success',
        'tx_id': str(tx.signatures[0])
    }