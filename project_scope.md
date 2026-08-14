# Description

As an implementation proposal, the primary objective of this project is to demonstrate how a Merkle Tree is able to ensure the integrity of the data stored within a Blockchain structure, through a proof of concept that functionally implements the basic structures of a Blockchain and visualizes its data.

The implemented proof of concept achieves the secondary objective of the project, which is to demonstrate the feasibility of carrying out an implementable, potentially functional, scalable Blockchain project that is free and open source software (FOSS) and applies the cybersecurity techniques and concepts discussed in this class.

For the MVP of this project, a series of points are generalized that are specifically sought to be covered, and others that, also specifically, are not implemented.

## What it covers

The Mini Blockchain Visualizer MVP covers the following elements:
- Manual Transaction Creation
- Grouping of Transactions into Blocks (every 4 Transactions)
- Merkle Tree Construction and Merkle Root Calculation
- Linked Block Lists with Hashes (Blockchain LinkedList + Hash Pointers)
- Tamper Detection
- Proof of Membership

The main reasons for its implementation are:
- Data structures with hash function calculations. Basic functionality within the Blockchain concept.
	- Transactions
	- Blocks
- Central focus on the topic (Post-Quantum Cryptography), stemming from the presentation of the Introduction to Cryptography course, essential for completing the topic of Post-Quantum Cryptography.
	- Merkle Tree and Merkle Root
- Demonstration of various cryptographic concepts, as well as demonstrating how to ensure data integrity.
	- Tamper Detection
	- Proof of Membership
	
## What it doesn't cover

- P2P Network (Multiple Nodes, Distributed Consensus, Real/Functional Cryptocurrency)
- Digital Signature of Transactions
- Mempool of Pending Transactions
- Mining
- Persistence (Blockchain Lives in Memory)
- Public API of a production Blockchain

The main reasons for not covering these topics are as follows:
- Outside the scope of the Introduction to Cryptography course.
	- P2P Network
	- Distributed Ledger
	- Mining
- The MVP transactions are merely illustrative.
	- Digital Signature of Transactions
- A typical Blockchain node network is not implemented; it is merely an illustrative structure for the MVP. Transactions reside in a pending mempool for each block. They only exist in memory.
	- Mempool
	- Persistence
- The concrete long-term scope of the project has not been defined, beyond being a FOSS project of a blockchain visualizer at first.
	- Public API