from .block import Block
from urllib.parse import urlparse
from itertools import chain


class Blockchain(object):

    REWARD = 5

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.nodes = set()

        # Create initial block
        self.add_block(previous_hash='1', proof='100')

    def register_node(self, address: str) -> None:
        """
        Register new node to the list of blockchain nodes.

        Parameters:
        ------------------------------------------------------
        address: str -> URL address of new blockchain node.
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        print(self.nodes)

    def add_block(self, previous_hash: str, proof: str, node_identifier: str | None = None) -> Block:
        """
        Adds new Block to the chain.

        Parameters:
        ------------------------------------------------------
        previous_hash: str -> Hash of the previous Block.
        proof: str -> Proof given by Proof of Work algorithm.

        Returns:
        ------------------------------------------------------
        Block -> New Block object.
        """

        # if len(self.pending_transactions) > Block.MAX_TRANSACTIONS_NUMBER:
        #     transactions = self.pending_transactions[:Block.MAX_TRANSACTIONS_NUMBER]
        #     self.pending_transactions = self.pending_transactions[Block.MAX_TRANSACTIONS_NUMBER:]
        # else:
        #     transactions = self.pending_transactions
        #     self.pending_transactions = []

        transactions = self.pending_transactions
        self.pending_transactions = []

        block = Block(
            index=len(self.chain) + 1,
            previous_hash=previous_hash,
            transactions=transactions,
            proof=proof
        )

        self.chain.append(block)
        if node_identifier:
            self.add_transaction(amount=Blockchain.REWARD, recipient=node_identifier)
        return block

    def add_transaction(self, amount: float, recipient: str, sender: str | None = None) -> int:
        """
        Creates new transaction and adds it to list of pending transactions.

        Parameters:
        ------------------------------------------------------
        sender: str | None (Optional) -> Address of the sender.
        amount: float -> Amount of currency to be transfered.
        recipient: str -> Address of the recipient.

        Returns:
        ------------------------------------------------------
        int -> Index of the Block which will hold the transaction.
        """

        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        last_block = self.get_last_block()
        return last_block.index + 1 if last_block else 1

    def get_last_block(self) -> Block:
        """
        Returns last Block in the chain.

        Returns:
        ------------------------------------------------------
        Block -> Last Block in the chain.
        """
        return self.chain[-1]

    def get_all_blocks(self) -> list[dict]:
        """
        Returns list of all Blocks in chain as a list of dictionaries.

        Returns:
        ------------------------------------------------------
        list[dict] -> List of all block as dictionaries.
        """
        return [block.to_dict() for block in self.chain]

    def get_all_transactions(self) -> list[dict]:
        """
        Returns list of all pending transactions as a list of dictionaries.

        Returns:
        ------------------------------------------------------
        list[dict] -> List of all pending transactions as dictionaries.
        """
        return self.pending_transactions

    def check_wallet_status(self, address: str) -> float:
        """
        Returns state of wallet of the given node address.

        Parameters:
        ------------------------------------------------------
        address: str -> Address of the node.

        Returns:
        ------------------------------------------------------
        float -> State of wallet.

        """
        wallet_status = 0
        transactions = list(chain.from_iterable([block.transactions for block in self.chain]))

        for transaction in transactions:
            if transaction["recipient"] == address:
                wallet_status += transaction["amount"]
            elif transaction["sender"] == address:
                wallet_status -= transaction["amount"]
        return wallet_status


if __name__ == '__main__':
    pass
