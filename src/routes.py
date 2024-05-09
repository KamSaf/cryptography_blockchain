from flask import Blueprint, request
from .config import app
from src.utils.blockchain import Blockchain
from uuid import uuid4
import json
from src.utils.block import Block

routes_bp = Blueprint('routes', __name__)
NODE_IDENTIFIER = str(uuid4()).replace('-', '')
BLOCKCHAIN = Blockchain()


# TODO dzielenie transakcji, zaawansowanie usuwanie transakcji przy tworzeniu bloku, nasłuchiwanie przed kazdą iteracji kopania, dodać fee przy kopaniu, sprawdzanie czy sender nie jest bankrutem


@app.route('/mine', methods=['GET'])
def mine():
    if len(BLOCKCHAIN.pending_transactions) == 0:
        return {"status_code": 204, "message": "No pending transactions."}

    previous_block = BLOCKCHAIN.get_last_block()
    proof = Block.proof_of_work(previous_proof=previous_block.proof)
    BLOCKCHAIN.add_block(previous_hash=previous_block.hash(), proof=proof, node_identifier=NODE_IDENTIFIER)
    return {"status_code": 201, "detail": "New block created!"}


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    if not request.get_data():
        return {"status_code": 400, "detail": "No data given"}
    request_data = json.loads(request.get_data().decode().replace('\'', '\"'))
    if "nodes" not in request_data.keys():
        return {"status_code": 400, "detail": "No node address given"}
    nodes = request_data["nodes"]
    for node in nodes:
        BLOCKCHAIN.register_node(address=node)
    return {"status_code": 201, "detail": "New nodes has been registered!"}


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    if not request.get_data():
        return {"status_code": 400, "detail": "No data given"}
    request_data = json.loads(request.get_data().decode().replace('\'', '\"'))
    if "recipient" not in request_data.keys():
        return {"status_code": 400, "detail": "No recipient address given"}
    if "amount" not in request_data.keys():
        return {"status_code": 400, "detail": "No amount given"}

    try:
        amount = float(request_data["amount"])
    except Exception:
        return {"status_code": 422, "detail": "Invalid amount data type (needs to be numeric)"}

    sender = request_data["sender"] if "sender" in request_data.keys() else '-'
    try:
        block_index = BLOCKCHAIN.add_transaction(sender=sender, amount=amount, recipient=request_data["recipient"])
        return {"status_code": 200, "detail": f"Transaction successfully assigned to Block {block_index}"}
    except Exception:
        return {"status_code": 500, "detail": "Unexpected error occured"}


@app.route('/transactions', methods=['GET'])
def get_transactions():
    return {
        "status_code": 200,
        "pending_transactions": BLOCKCHAIN.pending_transactions,
        "transactions_number": len(BLOCKCHAIN.pending_transactions)
    }


@app.route('/nodes', methods=['GET'])
def get_nodes():
    return {
        "status_code": 200,
        "nodes": list(BLOCKCHAIN.nodes),
        "nodes_number": len(BLOCKCHAIN.nodes)
    }


@app.route('/chain', methods=['GET'])
def get_full_chain():
    return {
        "status_code": 200,
        "chain": BLOCKCHAIN.get_all_blocks(),
        "length": len(BLOCKCHAIN.chain)
    }


@app.route('/wallet', methods=['GET'])
def get_wallet_status():
    return {
        "status_code": 200,
        "node_identifier": NODE_IDENTIFIER,
        "wallet_state": BLOCKCHAIN.check_wallet_status(address=NODE_IDENTIFIER)
    }


if __name__ == '__main__':
    pass
