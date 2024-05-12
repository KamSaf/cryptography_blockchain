from flask import Flask
from uuid import uuid4
from src.utils.blockchain import Blockchain


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e43f3561e5a94e365872c8c1eae6b576bd4ef308e7f31928'
NODE_IDENTIFIER = str(uuid4()).replace('-', '')
BLOCKCHAIN = Blockchain()

if __name__ == '__main__':
    pass
