## Description

Blockchain cryptocurrency application created for Cryptography classes.
This application offers both frontend and backend interfaces for interaction with the blockchain.

YoinkCoin allows users to create new transactions and mine blocks in which they are stored in a blockchain architecture.


## Technologies and tools used:

- Python 3.10
- Flask 3.0.3,
- requests 2.31.0,
- JavaScript,
- Bootstrap5 5.3.3,


## How to install (for Linux, macOS)

Create Python virtual environment, for example:

        virtualenv venv

Activate virtual environment:

        source venv/bin/activate

Run this command to install required dependencies

        pip install -r requirements.txt


## How to run

To start application run:

        python app.py


## API Endpoints


| **METHOD** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | **ENDPOINT** | **ACTION** | ***Parameters*** |
| ------------- | ------------- | ------------- | ------------- |
| ```/api``` | ```GET``` | Returns list of avaible endpoints. | N/A |
| ```/api/transactions``` | ```GET``` | Returns list of currently pending transactions. | N/A |
| ```/api/nodes``` | ```GET``` | Returns list of registered endpoints. | N/A |
| ```/api/nodes/resolve``` | ```GET``` | Syncs this nodes blockchain with registered nodes. | N/A |
| ```/api/chain``` | ```GET``` | Returns full blockchain. | N/A |
| ```/api/wallet``` | ```GET``` | Returns wallet state of this node. | N/A |
| ```/api/mine``` | ```GET``` | Mines new block. | N/A |
| ```/api/transactions/new``` | ```POST``` | Adds new pending transaction to the blockchain. | ```sender```, ```recipient```, ```amount``` |
| ```/api/nodes/register``` | ```POST``` | Registers new node address. | ```nodes``` |
| ```/api/testing/grant``` | ```POST``` | ***TESTING*** Grants 100 YoinkCoins to this node.  | N/A |
