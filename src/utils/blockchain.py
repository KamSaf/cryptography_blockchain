from .block import Block
from urllib.parse import urlparse
from itertools import chain
import requests
from time import time


class Blockchain(object):

    REWARD = 1

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.nodes = set()

        # Create initial block
        self.add_block(previous_hash='1', proof='100')

    @staticmethod
    def from_dict(blockchain_data: list) -> list[Block]:
        """
        Converts list of Block dictionaries into list of objects.

        Parameters:
        ------------------------------------------------------
        blockchain_data: list -> List of Blocks as dictionaries.

        Parameters:
        ------------------------------------------------------
        list[Block] -> List of Blocks as objects.
        """
        chain_of_objects = []
        for block in blockchain_data:
            chain_of_objects.append(Block.from_dict(block_dict=block))
        return chain_of_objects

    def is_node_registered(self, node_or_nodes: str | list[str]) -> bool:
        """
        Checks if node/nodes are already registered.

        Parameters:
        ------------------------------------------------------
        node_or_nodes: str | list[str] -> URL address or list of URL addresses.

        Returns:
        ------------------------------------------------------
        bool -> True if node/nodes are registered, False if not.

        """
        if type(node_or_nodes) is str:
            return urlparse(node_or_nodes).netloc in self.nodes

        for node in node_or_nodes:
            if urlparse(node).netloc in self.nodes:
                return True
        return False

    def register_node(self, address: str) -> None:
        """
        Register new node to the list of blockchain nodes.

        Parameters:
        ------------------------------------------------------
        address: str -> URL address of new blockchain node.
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

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
            'amount': amount,
            'creation_date': time(),
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

    def check_transaction_possible(self, sender: str, amount: float) -> bool:
        """
        Checks if transaction is possible (if sender is capable of sending given amount of money).

        Parameters:
        ------------------------------------------------------
        sender: str -> Address of transaction sender.
        amount: float -> Amount of money to be transfered.

        Returns:
        ------------------------------------------------------
        bool -> True if transaction possible, False if not.
        """
        sender_wallet_status = self.check_wallet_status(address=sender)
        return sender_wallet_status - amount >= 0

    def valid_chain(self, chain: list) -> bool:
        """
        Determine if a given blockchain is valid.

        Parameters:
        ------------------------------------------------------
        chain: list[dict] -> List of Blocks as dictionaries.

        Returns:
        ------------------------------------------------------
        bool -> True if valid, False if not.
        """
        chain = Blockchain.from_dict(blockchain_data=chain)
        previous_block = chain[0]

        for i in range(1, len(chain)):
            block = chain[i]
            if block.previous_hash != previous_block.hash():
                return False
            if not Block.valid_proof(previous_proof=previous_block.proof, proof=block.proof):
                return False

            previous_block = block
        return True

    def resolve_conflicts(self) -> bool:
        """
        Resolves conflicting chains in the blockchain network, replaces chain with the longest valid one.

        Returns:
        ------------------------------------------------------
        bool -> True if chain was replaced, False if not.
        """
        neighbours = self.nodes
        new_chain = None
        min_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code != 200:
                continue

            length = response.json()['length']
            chain = response.json()['chain']
            if length > min_length and self.valid_chain(chain=chain):
                min_length = length
                new_chain = chain

        if new_chain:
            self.chain = Blockchain.from_dict(blockchain_data=new_chain)
            return True

        return False


if __name__ == '__main__':
    pass
