import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QWidget, QFormLayout, QMessageBox
from cryptocurrency import Cryptocurrency

class CryptoGUI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = QMainWindow()
        self.crypto = Cryptocurrency()

    def setup_ui(self):
        self.main_window.setWindowTitle('Cryptocurrency Application')

        central_widget = QWidget()
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.sender_edit = QLineEdit()
        self.recipient_edit = QLineEdit()
        self.amount_edit = QLineEdit()

        form_layout.addRow(QLabel('Sender:'), self.sender_edit)
        form_layout.addRow(QLabel('Recipient:'), self.recipient_edit)
        form_layout.addRow(QLabel('Amount:'), self.amount_edit)

        button_layout = QHBoxLayout()
        self.create_transaction_button = QPushButton('Create Transaction')
        self.mine_transactions_button = QPushButton('Mine Transactions')
        self.show_blockchain_button = QPushButton('Show Blockchain')

        button_layout.addWidget(self.create_transaction_button)
        button_layout.addWidget(self.mine_transactions_button)
        button_layout.addWidget(self.show_blockchain_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        central_widget.setLayout(layout)
        self.main_window.setCentralWidget(central_widget)

        self.create_transaction_button.clicked.connect(lambda: self.create_transaction())
        self.mine_transactions_button.clicked.connect(lambda: self.mine_transactions())
        self.show_blockchain_button.clicked.connect(lambda: self.show_blockchain())

    def create_transaction(self):
        try:
            sender = self.sender_edit.text()
            recipient = self.recipient_edit.text()
            amount = float(self.amount_edit.text())
            transaction = self.crypto.create_transaction(sender, recipient, amount, time.time())
            QMessageBox.about(QWidget(), "Success", f'Transaction created: {transaction.__dict__}')


            self.sender_edit.clear()
            self.recipient_edit.clear()
            self.amount_edit.clear()

        except Exception as e:
            QMessageBox.about(QWidget(), "Error", "Invalid input")

    def mine_transactions(self):
        try:
            new_block = self.crypto.mine_pending_transactions()
            QMessageBox.about(QWidget(), "Success", f'New block mined: {new_block.__dict__}')

        except Exception as e:
            QMessageBox.about(QWidget(), "Error", str(e))

    def show_blockchain(self):
        QMessageBox.about(QWidget(), "Blockchain", str(self.crypto.blockchain))

    def run(self):
        self.setup_ui()
        self.main_window.show()
        sys.exit(self.app.exec_())
