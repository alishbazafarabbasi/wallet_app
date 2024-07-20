from solders.keypair import Keypair
import binascii
from mnemonic import Mnemonic

def create_keypair_from_secret(private_key_hex):
    try:
        # Convert the private key from hex to bytes
        private_key_bytes = binascii.unhexlify(private_key_hex)
        # Create a keypair from the private key bytes
        keypair = Keypair.secret(private_key_bytes)
        return keypair
    except Exception as e:
        raise ValueError(f"Invalid private key: {e}")



def mnemonic_to_seed(mnemonic_phrase, passphrase=''):
    mnemo = Mnemonic("english")
    seed = mnemo.to_seed(mnemonic_phrase, passphrase)
    return seed

def seed_to_keypair(seed):
    # Generate a keypair from the seed
    keypair = Keypair.from_seed(seed[:32])
    return keypair
def create_keypair_from_secret_key(secret_key_input):
    try:
        # Convert the comma-separated string to a list of integers
        secret_key = list(map(int, secret_key_input.split(',')))

        # Check if the secret key is exactly 32 or 64 bytes long
        if len(secret_key) not in [32, 64]:
            raise ValueError("Secret key must be 32 or 64 bytes long.")
        
        # Convert list of integers to bytes
        secret_key_bytes = bytes(secret_key)

        # Create Keypair from the secret key
        if len(secret_key_bytes) == 32:
            keypair = Keypair.from_seed(secret_key_bytes)
        else:
            keypair = Keypair.from_bytes(secret_key_bytes)
        return keypair
    except ValueError as e:
        raise ValueError(f"Invalid secret key: {e}")
    except Exception as e:
        raise ValueError(f"Error processing secret key: {e}")
