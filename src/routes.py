from flask import Blueprint, request
from .config import app
from src.utils.blockchain import Blockchain
from uuid import uuid4
import json
from src.utils.block import Block

routes_bp = Blueprint('routes', __name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()


# TODO dzielenie tranzakcji, zaawansowanie usuwanie tranzakcji przy tworzeniu bloku,


@app.route('/mine', methods=['GET'])
def mine():
    if len(blockchain.pending_transactions) == 0:
        return {"status_code": 204, "message": "No pending transactions."}

    previous_block = blockchain.get_last_block()
    proof = Block.proof_of_work(previous_proof=previous_block.proof)
    blockchain.add_block(previous_hash=previous_block.hash(), proof=proof, node_identifier=node_identifier)
    return {"status_code": 201, "detail": "New block created!"}


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    if not request.get_data():
        return {"status_code": 400, "detail": "No data send"}
    request_data = json.loads(request.get_data().decode().replace('\'', '\"'))
    if "recipient" not in request_data.keys():
        return {"status_code": 400, "detail": "No recipient address given send"}
    if "amount" not in request_data.keys():
        return {"status_code": 400, "detail": "No amount given"}

    try:
        amount = float(request_data["amount"])
    except Exception:
        return {"status_code": 422, "detail": "Invalid amount data type (needs to be numeric)"}

    sender = request_data["sender"] if "sender" in request_data.keys() else '-'
    try:
        block_index = blockchain.add_transaction(sender=sender, amount=amount, recipient=request_data["recipient"])
        return {"status_code": 200, "detail": f"Transaction successfully assigned to Block {block_index}"}
    except Exception:
        return {"status_code": 500, "detail": "Unexpected error occured"}


@app.route('/transactions', methods=['GET'])
def get_transactions():
    return {
        "status_code": 200,
        "pending_transactions": blockchain.pending_transactions,
        "transactions_number": len(blockchain.pending_transactions)
    }


@app.route('/chain', methods=['GET'])
def get_full_chain():
    return {
        "status_code": 200,
        "chain": blockchain.get_all_blocks(),
        "length": len(blockchain.chain)
    }
