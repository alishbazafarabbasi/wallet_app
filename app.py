from flask import Flask
from config import Config
from routes.wallet_routes import wallet_bp
from routes.transaction_routes import transaction_bp

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(wallet_bp)

# Register Blueprints
# app.register_blueprint(wallet_bp)
app.register_blueprint(transaction_bp)

if __name__ == '__main__':
    app.run(debug=True)
