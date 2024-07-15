def create_keypair_from_secret(secret_key_input):
    try:
        secret_key = list(map(int, secret_key_input.split(',')))
        return secret_key
    except ValueError:
        return None