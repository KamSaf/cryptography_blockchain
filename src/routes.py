from flask import Blueprint, request
from .config import app
from src.utils.blockchain import Blockchain
from uuid import uuid4
import json
from src.utils.block import Block

API_ROUTES_BP = Blueprint('api_routes', __name__)
NODE_IDENTIFIER = str(uuid4()).replace('-', '')
BLOCKCHAIN = Blockchain()


# TODO nasłuchiwanie przed kazdą iteracji kopania, sprawdzanie czy sender nie jest bankrutem
# na potrzeby testowania endpoint, który daje użytkownikowi 100 monet


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
    if "sender" not in request_data.keys():
        return {"status_code": 400, "detail": "No sender address given"}
    if "amount" not in request_data.keys():
        return {"status_code": 400, "detail": "No amount given"}

    try:
        amount = float(request_data["amount"])
    except Exception:
        return {"status_code": 422, "detail": "Invalid amount data type (needs to be numeric)"}

    try:
        block_index = BLOCKCHAIN.add_transaction(sender=request_data["sender"], amount=amount, recipient=request_data["recipient"])
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


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = BLOCKCHAIN.resolve_conflicts()

    if replaced:
        response = {
            'status_code': 200,
            'message': 'Chain was replaced',
        }
    else:
        response = {
            'status_code': 200,
            'message': 'This chain is authoritative',
        }

    return response


if __name__ == '__main__':
    pass
