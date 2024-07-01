import os
import ecdsa
import hashlib
from cryptography.fernet import Fernet

def generate_private_key():
    return os.urandom(32)

def private_key_to_public_key(private_key):
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return b'\04' + vk.to_string()

def public_key_to_address(public_key):
    sha256_1 = hashlib.sha256(public_key).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_1)
    return ripemd160.hexdigest()

def generate_encryption_key():
    return Fernet.generate_key()

def encrypt_private_key(private_key, encryption_key):
    f = Fernet(encryption_key)
    encrypted_key = f.encrypt(private_key)
    return encrypted_key

def decrypt_private_key(encrypted_key, encryption_key):
    f = Fernet(encryption_key)
    decrypted_key = f.decrypt(encrypted_key)
    return decrypted_key
