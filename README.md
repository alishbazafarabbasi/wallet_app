# Blockchain Wallet App

## Overview

The **Blockchain Wallet** project is a web application designed for managing Solana blockchain wallets. Users can create new wallets, log in to existing ones, view wallet details, request tokens from a faucet, check wallet balances, and transfer SOL (Solana cryptocurrency) between addresses.

## Features

- **Create Wallet**: Generate a new wallet with a mnemonic phrase.
- **Login to Wallet**: Access an existing wallet using a mnemonic phrase.
- **View Wallet Details**: Check wallet address, public key, private key, and mnemonic phrase.
- **Request Tokens**: Request tokens from the Solana faucet.
- **Get Wallet Balance**: View the current balance of your wallet.
- **Transfer SOL**: Send SOL between addresses using the sender’s private key.

## How to Use

### Creating a New Wallet

1. Navigate to the **Create Wallet** page.
2. Choose the language for the mnemonic phrase (English or Chinese Simplified).
3. Click on **Create Wallet** to generate a new wallet.
4. Save the mnemonic phrase securely. You will need it to log in to your wallet.

### Logging into an Existing Wallet

1. Go to the **Login to Wallet** page.
2. Enter your mnemonic phrase in the provided textarea.
3. Click on **Login** to access your wallet.

### Viewing Wallet Details

1. After logging in, you will be redirected to the **Wallet Details** page.
2. Here, you can view your wallet address, public key, private key, and mnemonic phrase.
3. Use the provided forms to request tokens from the faucet or to check your wallet balance.

### Requesting Tokens from the Faucet

1. On the **Wallet Details** page, find the **Request Tokens from Faucet** button.
2. Click the button to request tokens.

### Checking Wallet Balance

1. On the **Wallet Details** page, click the **Get Wallet Balance** button.
2. The current balance will be displayed on the page.

### Transferring SOL

1. On the **Wallet Details** page, locate the **Transfer SOL** section.
2. Enter the recipient's address, amount of SOL to send, and your private key.
3. Click on **Transfer** to initiate the transaction.
4. Transaction details including transaction ID, recent blockhash, and status will be displayed.

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
2. Enter your mnemonic phrase and click **login**.
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
