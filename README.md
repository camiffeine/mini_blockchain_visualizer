# Mini Merkle Blockchain Visualizer

A simple proof-of-concept blockchain explorer that demonstrates **Merkle Tree integrity verification**, **tamper detection**, and **proof of membership** in an interactive web interface.

Built for educational purposes to illustrate cryptographic concepts for my *Introduction to Cryptography and Information Security* course at uni.

## Overview

This is a simple yet functional blockchain implementation focused on demonstrating how **Merkle Trees** ensure data integrity. The application provides a simple visual, interactive interface to:

- Create illustrative transactions manually
- Group transactions into blocks (automatic at 4 transactions)
- Inspect Merkle tree structures and generate proof paths
- Detect tampering with transactions and verify chain integrity
- Explore the entire blockchain state in real-time

This course project was developed with the objective of demonstrating real-world applications of the following concepts:

- **Cryptographic Hashing**: Applying secure hashing with SHA256, and reviewing possible migration to future algorithms.
- **Merkle Trees**: As an efficient proof of membership.
- **Blockchain Fundamentals**: Linked blocks with hash pointers, block headers.
- **Data Structures**: Including linkedList, binary trees, hashing.
- **API Design**: Web development fundamentals including RESTful endpoints, validation, error handling.

### Features

- **Manual Transaction Creation**: Add transactions with sender, receiver, amount, and metadata  
- **Automatic Block Creation**:  Packages pending transactions into blocks  
- **Merkle Tree Visualization**:  Interactive tree view with proof generation  
- **Tamper Detection**:  Modify a transaction and observe integrity failure  
- **Proof of Membership**:  Verify any transaction's authentication path  
- **Dashboard**:  Monitor chain health, pending transactions, and block status  
- **REST API**:  Full-featured FastAPI backend with automatic Swagger documentation  

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (HTML/JS/CSS)                  │
│  Dashboard | Blockchain | Block Details | Merkle Tree View  │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               FastAPI Backend (Python)                      │
│  ┌──────────────────┐  ┌──────────────────────────────────┐ │
│  │ Routes Layer     │  │ Services Layer                   │ │
│  │ ├─ /transactions │  │ ├─ BlockchainService             │ │
│  │ ├─ /blockchain   │  │ └─ Schema validation             │ │
│  │ └─ /merkle-proof │  └──────────────────────────────────┘ │
│  └──────────────────┘                                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │    Core Business Logic         │
        │  ┌──────────────────────────┐  │
        │  │ Blockchain               │  │
        │  │ ├─ Transaction Pool      │  │
        │  │ ├─ LinkedList (Chain)    │  │
        │  │ └─ Block Management      │  │
        │  └──────────────────────────┘  │
        │  ┌──────────────────────────┐  │
        │  │ Cryptography             │  │
        │  │ ├─ SHA256 Hashing        │  │
        │  │ └─ Merkle Tree/Proofs    │  │
        │  └──────────────────────────┘  │
        └────────────────────────────────┘
```

The following Architecture Principles have been considered during the implementation

- **Layered Design**: Separation of concerns between routes, services, and core logic.
- **In-Memory State**: All blockchain data lives in memory (no database required for the project's scope).
- **Immutable Blocks**: Blocks are immutable after creation; transactions can only be tampered in-place for demonstrative and illustrative purposes.
- **Hash-Based Integrity**: All data structures are secured with SHA256 cryptographic hashing by default.


## Quick Start

### Prerequisites

- Python 3.9+ installed
- pip package manager

### Installation and Running the Application

1. **Clone the repository**
   ```bash
   git clone https://github.com/camiffeine/mini_merkle_blockchain.git
   cd mini_merkle_blockchain
   ```

2. **Setup the virtual environment using uv**
   ```bash
   uv init --bare
   uv add -r backend/requirements.txt
   uv sync
   ```

3. **Activate the virtual environment**
   ```bash
   # Windows
   .\.venv\Scripts\Activate.ps1

   # Bash
    source .venv/bin/activate
   ```

4. **Start the backend server:**
   ```bash
   # Windows
   fastapi dev .\backend\app\main.py

   # Bash
   fastapi dev backend/app/main.py
   ```

   **Open your browser and visit your localhost:**
   ```bash
   http://127.0.0.1:8000
   ```

   The frontend will load automatically. The dashboard displays live blockchain status.

## Walkthrough

### 1. **Create a Transaction**
- Navigate to the **Dashboard** tab
- Fill in the transaction form: Sender, Receiver, Amount
- Click "Add transaction"
- The transaction appears in the "Pending transactions" panel

### 2. **Create a Block**
- Once you have ≥1 pending transactions, click "Create block" in the Quick Actions section
- A new block is automatically generated from the pending pool
- The blockchain chain length increases

### 3. **Inspect Block Details**
- Navigate to the **Blockchain** tab to see all blocks
- Click "View details" on any block to see:
  - Block header (index, timestamp, nonce, difficulty)
  - Complete hash (merkle root, block hash, previous hash)
  - All transactions in the block

### 4. **Tamper with a Transaction**
- In the **Block Details** view, scroll to "Tamper transaction"
- Select a transaction index and modify its fields
- Click "Apply tamper"
- Return to **Blockchain** view to observe:
  - Block validation status changes to `Invalid`
  - Block hash no longer matches the stored hash
  - This demonstrates integrity detection

### 5. **Verify Merkle Proof**
- Navigate to the **Merkle Tree** tab
- The tree visualization shows all leaves (transactions) and internal nodes
- In the "Merkle proof" section:
  - Select a transaction index
  - Click "Verify proof"
  - The proof shows the authentication path from leaf to root
  - Status indicator shows `Valid proof` if the path authenticates correctly

## API Endpoints

The backend exposes a RESTful API with automatic documentation available at `http://127.0.0.1:8000/docs` (Swagger UI).

### Blockchain Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/blockchain/status` | Get blockchain status (valid, chain length, last block hash) |
| `GET` | `/blockchain` | Get entire blockchain structure |
| `GET` | `/blockchain/blocks` | Create a new block from pending transactions |
| `GET` | `/blockchain/blocks/{index}` | Get a specific block by index |

### Transaction Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/transactions/add` | Add a new transaction to the pending pool |
| `POST` | `/transactions/tamper` | Modify a transaction in a block (demo only) |

### Merkle Proof Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/blockchain/blocks/{block_index}/transactions/{transaction_index}/merkle-proof` | Generate a Merkle proof for a transaction |

## Security & Integrity

### How Merkle Trees Ensure Integrity

1. **Leaf Hashing**: Each transaction is hashed (SHA256)
2. **Tree Construction**: Pairs of hashes are combined and hashed upward
3. **Root Hash**: Final root hash is stored in the block header
4. **Tampering Detection**: Modifying any transaction changes the path up to the root, invalidating the block

### Proof of Membership

The application can generate a **Merkle proof** for any transaction:
- **Proof**: A minimal set of sibling hashes needed to recompute the root
- **Verification**: Follow the path from leaf to root using proof steps
- **Efficiency**: O(log n) proof size, where n = number of transactions

## License

This project is currently under the **GPL 3.0 License**. See [LICENSE](LICENSE) for details.


**Last Updated**: 2026-08-15