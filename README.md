# Blockchain Wallet

## Overview

The **Blockchain Wallet** project is a web application that allows users to manage Solana blockchain wallets. This app provides features for creating new wallets, viewing wallet details, requesting tokens from a faucet, checking wallet balances, and transferring SOL (Solana cryptocurrency) between addresses.

## Features

- **Create Wallet**  
  Generate a new Solana wallet and view its details.

- **View Wallet Details**  
  Display the wallet's name, address, and public key.

- **Request Tokens**  
  Request tokens from the Solana faucet.

- **Get Wallet Balance**  
  Fetch and display the balance of a wallet.

- **Transfer SOL**  
  Send SOL from one wallet to another.

## Technologies Used

- **Frontend:**  
  HTML, CSS, JavaScript

- **Backend:**  
  Flask (Python)

- **Blockchain:**  
  Solana

## Usage

### Create Wallet

1. Navigate to the **_Create Wallet_** page at the root URL (`/`).
2. Enter a name for the wallet and click **_Create Wallet_**.
3. A new wallet will be created, and you will be redirected to the wallet details page.

### View Wallet Details

- The wallet details page displays the wallet's name, address, and public key.

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
