import hashlib
import json

def validate_transaction(transaction):
    if transaction.sender and transaction.recipient and transaction.amount > 0:
        return True
    return False

def proof_of_work(blockchain, transactions, difficulty=4):
    nonce = 0
    new_block = blockchain.create_new_block(nonce, transactions)
    target = '0' * difficulty

    while new_block.hash[:difficulty] != target:
        nonce += 1
        new_block = blockchain.create_new_block(nonce, transactions)

    return nonce

def hash_block(block):
    block_string = json.dumps(block.__dict__, sort_keys=True)
    return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

cryptocurrency.py:
from blockchain import Blockchain
from utilities import validate_transaction, proof_of_work


class Transaction:
    def __init__(self, sender, recipient, amount, timestamp):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp


class Cryptocurrency:
    def __init__(self):
        self.blockchain = Blockchain()

    def create_transaction(self, sender, recipient, amount, timestamp):
        transaction = Transaction(sender, recipient, amount, timestamp)

        if not validate_transaction(transaction):
            raise ValueError("Invalid transaction")

        self.blockchain.add_transaction(transaction)
        return transaction

    def mine_pending_transactions(self):
        if not self.blockchain.pending_transactions:
            raise Exception("No pending transactions to mine")

        nonce = proof_of_work(self.blockchain, self.blockchain.pending_transactions)
        new_block = self.blockchain.create_new_block(nonce, self.blockchain.pending_transactions.copy())

        self.blockchain.add_block(new_block)
        self.pending_transactions = []

        return new_block
