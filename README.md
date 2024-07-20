# Blockchain Wallet

## Overview

The **Blockchain Wallet** project is a web application designed for managing Solana blockchain wallets. Users can create new wallets, view wallet details, request tokens from a faucet, check wallet balances, and transfer SOL (Solana cryptocurrency) between addresses.

## Features

- **Create Wallet**: Generate a new Solana wallet and view its details.
- **Login Wallet**: Log in to an existing wallet using a secret key.
- **View Wallet Details**: Display the wallet's address, public key, private key, and optionally the secret key and mnemonic phrase.
- **Request Tokens**: Request tokens from the Solana faucet.
- **Get Wallet Balance**: Fetch and display the balance of a wallet.
- **Transfer SOL**: Send SOL from one wallet to another.
- **Generate Mnemonics**: Create a mnemonic phrase to be used for wallet creation.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Blockchain**: Solana

## Installation

1. **Clone the Repository**:
   `git clone https://github.com/yourusername/blockchain-wallet.git`
   `cd blockchain-wallet`

2. **Create a Virtual Environment:**:
   `python -m venv venv`
   `source venv/bin/activate`  # On Windows use `venv\Scripts\activate`

3. **Install Dependencies:**:
   `pip install -r requirements.txt`

3. **Run the Application**:
   `python app.py`

## Usage

### Create Wallet

1. Navigate to the **_Login Wallet_** page (`/login_wallet`).
2. Enter your secret key (comma-separated integers) and click **login**.
3. You will be redirected to the wallet details page.

### View Wallet Details

- The wallet details page displays the wallet's address, public key, private key, and optionally the secret key and mnemonic phrase.

### Request Tokens from Faucet

- Click on the **_Request Tokens from Faucet_** button on the wallet details page to request SOL tokens from the Solana faucet.

### Get Wallet Balance

- Click on the **_Get Wallet Balance_** button on the wallet details page to fetch and display the current balance of the wallet.

### Transfer SOL

1. Enter the sender's address, receiver's address, amount (in _lamports_), and sender's private key.
2. Click on the **_Transfer_** button to send SOL from the sender to the receiver.

## Recent Blockhash

### What is a Recent Blockhash?

- **Definition:** A recent blockhash is a unique identifier for the most recent block in the Solana blockchain, represented as a 32-byte value or a hexadecimal string.
- **Purpose:** It ensures the validity of transactions and prevents replay attacks by associating transactions with the most recent blockchain state.

### Role in Transactions

- **Transaction Validity:** Ensures transactions are valid and based on the latest blockchain state.
- **Transaction Confirmation:** Nodes verify transactions using the recent blockhash.
- **Preventing Replay Attacks:** Unique to the block it was created for, preventing transactions from being replayed.
