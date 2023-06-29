import hashlib
import json
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce, hash=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = hash if hash else self.calculate_hash()

    def calculate_hash(self):
        block_dict = self.__dict__.copy()
        block_dict['transactions'] = [transaction_to_dict(t) for t in block_dict['transactions']]
        block_string = json.dumps(block_dict, sort_keys=True)
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def __str__(self):
        blockchain_string = "Blockchain:\n"
        for block in self.chain:
            block_string = f"Block {block.index}:\n"
            block_string += f"  Previous Hash: {block.previous_hash}\n"
            block_string += f"  Timestamp: {block.timestamp}\n"
            block_string += f"  Nonce: {block.nonce}\n"
            block_string += f"  Hash: {block.hash}\n"
            block_string += "  Transactions:\n"

            for transaction in block.transactions:
                transaction_string = f"    Sender: {transaction.sender}, Recipient: {transaction.recipient}, Amount: {transaction.amount}, Timestamp: {transaction.timestamp}\n"
                block_string += transaction_string
            blockchain_string += block_string
        return blockchain_string

    def create_genesis_block(self):
        genesis_block = Block(0, '0', time.time(), [], 0)
        return genesis_block

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def create_new_block(self, nonce, transactions, previous_hash=None):
        block = Block(len(self.chain), previous_hash or self.get_latest_block().hash, time.time(), transactions, nonce)
        return block

    def add_block(self, block):
        if self.is_chain_valid():
            self.chain.append(block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

def transaction_to_dict(transaction):
    return transaction.__dict__
