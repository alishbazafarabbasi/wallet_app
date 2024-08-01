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


GITHUB_SECRET = os.environ.get('GITHUB_SECRET', '12345')

def verify_signature(payload, signature):

    secret = bytes(GITHUB_SECRET, 'utf-8')
    hashed = hmac.new(secret, payload, hashlib.sha1)
    expected_signature = 'sha1=' + hashed.hexdigest()
    return hmac.compare_digest(expected_signature, signature)

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_data()
    signature = request.headers.get('X-Hub-Signature')


    if not verify_signature(payload, signature):
        return jsonify({'error': 'Invalid signature'}), 403

    data = request.json
    event = request.headers.get('X-GitHub-Event')

    if event == 'push':

        print('Push event received:')
        print(data)

    elif event == 'pull_request':

        print('Pull request event received:')
        print(data)

    return jsonify({'status': 'Webhook received'}), 200

# Register Blueprints
# app.register_blueprint(wallet_bp)
app.register_blueprint(transaction_bp)

if __name__ == '__main__':
    app.run(debug=True)
