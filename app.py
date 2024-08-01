from flask import Flask, request, jsonify
from config import Config
from routes.wallet_routes import wallet_bp
from routes.transaction_routes import transaction_bp
import hmac
import hashlib
import os

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(wallet_bp)

app = Flask(__name__)

# Secret token for validating GitHub webhook requests
GITHUB_SECRET = os.environ.get('GITHUB_SECRET', 'iamalishba')

def verify_signature(payload, signature):
    """Verify the signature of the webhook payload."""
    secret = bytes(GITHUB_SECRET, 'utf-8')
    
    if signature.startswith('sha1='):
        hashed = hmac.new(secret, payload, hashlib.sha1)
        expected_signature = 'sha1=' + hashed.hexdigest()
    elif signature.startswith('sha256='):
        hashed = hmac.new(secret, payload, hashlib.sha256)
        expected_signature = 'sha256=' + hashed.hexdigest()
    else:
        return False
    
    return hmac.compare_digest(expected_signature, signature)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Read the raw payload from the request
    payload = request.get_data()
    signature = request.headers.get('X-Hub-Signature') or request.headers.get('X-Hub-Signature-256')

    if not signature:
        return jsonify({'error': 'Signature header missing'}), 400

    if not verify_signature(payload, signature):
        return jsonify({'error': 'Invalid signature'}), 403

    data = request.json
    event = request.headers.get('X-GitHub-Event')

    if event == 'push':
        print('Push event received:')
        print(data)
    else:
        print(f'Unhandled event: {event}')
        print(data)

    return jsonify({'status': 'Webhook received'}), 200

if __name__ == '_main_':
    app.run(port=3000, debug=True)


# Register Blueprints
# app.register_blueprint(wallet_bp)
app.register_blueprint(transaction_bp)

if __name__ == '__main__':
    app.run(debug=True)
