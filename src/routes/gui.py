from flask import Blueprint, render_template
from src.config import app, BLOCKCHAIN, NODE_IDENTIFIER

GUI_ROUTES_BP = Blueprint('gui_routes', __name__)


@app.route('/', methods=['GET'])
def main():
    return render_template(template_name_or_list='home.html')


@app.route('/transactions', methods=['GET'])
def gui_transactions():
    transactions = BLOCKCHAIN.pending_transactions
    transactions.reverse()
    return render_template(template_name_or_list='transactions.html', transactions=transactions)


@app.route('/nodes', methods=['GET'])
def gui_nodes():
    return render_template(template_name_or_list='nodes.html', nodes=list(BLOCKCHAIN.nodes).reverse())


@app.route('/wallet', methods=['GET'])
def gui_wallet_status():
    pending_transactions = []
    for transaction in BLOCKCHAIN.pending_transactions:
        if transaction['sender'] == NODE_IDENTIFIER or transaction['recipient'] == NODE_IDENTIFIER:
            pending_transactions.append(transaction)
    transactions = BLOCKCHAIN.transactions_history(address=NODE_IDENTIFIER)
    transactions.reverse()
    pending_transactions.reverse()
    return render_template(
        template_name_or_list='wallet.html',
        node_indentifier=NODE_IDENTIFIER,
        wallet_status=BLOCKCHAIN.check_wallet_status(address=NODE_IDENTIFIER),
        transactions=transactions,
        pending_transactions=pending_transactions.reverse()
    )


@app.route('/chain', methods=['GET'])
def gui_full_chain():
    return render_template(template_name_or_list='chain.html')
