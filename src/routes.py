from flask import Blueprint
from .config import app
from src.utils.blockchain import Blockchain
from uuid import uuid4

routes_bp = Blueprint('routes', __name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    if len(blockchain.pending_transactions) == 0:
        return {"message": "No pending transactions."}
    return {"message": "Hello!"}


@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    return {"message": "Hello!"}


@app.route('/chain', methods=['GET'])
def get_full_chain():
    return {
        "chain": blockchain.get_all_blocks(),
        "length": len(blockchain.chain)
    }
