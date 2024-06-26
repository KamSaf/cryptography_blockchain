from time import time
import json
import hashlib


class Block(object):

    MAX_TRANSACTIONS_NUMBER = 100
    ZERO_PADDING_LENGTH = 4

    def __init__(self, index: int, proof: str, previous_hash: str, transactions: list, timestamp: float | None = None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp if timestamp else time()
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
            'transactions': self.transactions,
            'proof': self.proof,
            'previous_hash': self.previous_hash
        }

    @staticmethod
    def from_dict(block_dict: dict) -> "Block":
        """
        Converts dict Block data into an object.

        Parameters:
        ------------------------------------------------------
        block_dict -> Block data as dictionary


        Returns:
        ------------------------------------------------------
        Block -> Block object
        """
        return Block(
            index=block_dict['index'],
            proof=block_dict['proof'],
            timestamp=block_dict['timestamp'],
            previous_hash=block_dict['previous_hash'],
            transactions=block_dict['transactions']
        )

    def hash(self) -> str:
        """
        Returns a SHA-256 hash of a Block.

        Returns:
        ------------------------------------------------------
        str -> Hash of the Block data
        """
        block_data = json.dumps(self.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(string=block_data).hexdigest()

    @staticmethod
    def proof_of_work(previous_proof: str) -> str:
        """
        Returns a number that meets the Proof of Work conditions, i.e. hash ends with required number of 0s.

        Parameters:
        ------------------------------------------------------
        previous_proof: str -> Proof of Work of the previous Block

        Returns:
        ------------------------------------------------------
        str -> Proof of work for new Block,
        """
        proof = 0
        while Block.valid_proof(previous_proof, proof) is False:
            proof += 1

        return str(proof)

    @staticmethod
    def valid_proof(previous_proof, proof) -> bool:
        """
        Checks if calculated hash starts with required number of 0s.

        Parameters:
        ------------------------------------------------------
        previous_proof: str -> Proof of Work of the previous Block
        proof: str -> Newly generated Proof of Work to be verified

        Returns:
        ------------------------------------------------------
        bool -> True if generated Proof of Work is valid,
        """
        guess = f'{previous_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:Block.ZERO_PADDING_LENGTH] == '0' * Block.ZERO_PADDING_LENGTH


if __name__ == '__main__':
    pass
