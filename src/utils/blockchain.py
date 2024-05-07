from .block import Block


class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        # Create initial block
        self.add_block(previous_hash='1', proof='100')

    def add_block(self, previous_hash: str, proof: str) -> Block:
        """
        Adds new Block to the chain.

        Parameters:
        ------------------------------------------------------
        previous_hash: str -> Hash of the previous Block
        proof: str -> Proof given by Proof of Work algorithm

        Returns:
        ------------------------------------------------------
        Block -> New Block object
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
            proof=proof,
            transactions=transactions,
        )

        self.chain.append(block)
        return block

    def add_transaction(self, sender: str, recipient: str, amount: float) -> int:
        """
        Creates new transaction and adds it to list of pending transactions.

        Parameters:
        ------------------------------------------------------
        sender: str -> Address of the sender.
        recipient: str -> Address of the recipient.
        amount: float -> Amount of currency to be transfered.

        Returns:
        ------------------------------------------------------
        int -> Index of the Block which will hold the transaction,
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
        Block -> Last Block in the chain
        """
        return self.chain[-1]
