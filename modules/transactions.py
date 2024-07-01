import json
import ecdsa

def create_transaction(sender, recipient, amount):
    if not sender or not recipient or amount <= 0:
        raise ValueError("Invalid transaction data")
    return {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }

def sign_transaction(transaction, private_key):
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    transaction_bytes = json.dumps(transaction, sort_keys=True).encode()
    return sk.sign(transaction_bytes).hex()
