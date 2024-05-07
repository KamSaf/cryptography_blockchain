from time import time
import json
import hashlib


class Block(object):

    MAX_TRANSACTIONS_NUMBER = 100
    ZERO_PADDING_LENGTH = 4

    def __init__(self, index: int, previous_hash: str, proof: str, transactions: list):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time()
        self.proof = proof
        self.transactions = transactions

    def to_dict(self) -> dict:
        """
        Returns Block data as a dictionary.

        Returns:
        ------------------------------------------------------
        dict -> Block data as dictionary
        """
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transaction': self.transactions,
            'proof': self.proof,
            'previous_hash': self.previous_hash
        }

    def hash(self) -> str:
        """
        Returns a SHA-256 hash of a Block.

        Parameters:
        ------------------------------------------------------
        block: str -> Address of the sender.

        Returns:
        ------------------------------------------------------
        str -> Hash of the Block,
        """
        block_data = json.dumps(self.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(string=block_data).hexdigest()

    def proof_of_work(self, previous_proof):
        """
        Returns a number that meets the Proof of Work conditions, i.e. hash ends with 4 zeros.

        Parameters:
        ------------------------------------------------------
        block: str -> Address of the sender.

        Returns:
        ------------------------------------------------------
        str -> Hash of the Block,
        """
        proof = 0
        while self.valid_proof(previous_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(previous_proof, proof):
        """
        """
        guess = f'{previous_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'
