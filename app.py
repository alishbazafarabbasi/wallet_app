from flask import Flask, request, jsonify
from config import Config
from routes.wallet_routes import wallet_bp
from routes.transaction_routes import transaction_bp

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(wallet_bp)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        if not data:
            raise ValueError("No JSON data received")

        app.logger.info(f"Received data: {data}")
        return jsonify({'message': 'Webhook received!'}), 200
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({'message': 'Error processing request'}), 400


# Register Blueprints
# app.register_blueprint(wallet_bp)
app.register_blueprint(transaction_bp)

if __name__ == '__main__':
    app.run(debug=True)
