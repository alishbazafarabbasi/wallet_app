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

def mnemonic_to_seed(mnemonic_phrase, passphrase='', language='english'):

    mnemo = Mnemonic(language)
    seed = mnemo.to_seed(mnemonic_phrase, passphrase)
    return seed

def seed_to_keypair(seed):
    # Ensure the seed is 32 bytes long
    keypair = Keypair.from_seed(seed[:32])
    return keypair

def generate_mnemonic(language='english'):
    mnemo = Mnemonic(language)
    return mnemo.generate(128)
