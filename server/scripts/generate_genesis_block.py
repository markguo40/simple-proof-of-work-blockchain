from Crypto.PublicKey import RSA
from server.models import Block, Account, Transaction
from blockchain.settings import GENESIS_ADDRESS
from Crypto.Signature import pss
from decimal import Decimal

print("Creating Genesis Account...")
genesis_account, created = Account.objects.get_or_create(address=GENESIS_ADDRESS)
genesis_account.balance = Decimal("100000000")
genesis_account.save()

print("Creating Genesis Transaction...")
genesis_transaction = Transaction.objects.create(sender=genesis_account, 
												amount=Decimal("100000000"),
												receiver=genesis_account,
												nonce=0)
genesis_transaction.transaction_hash = genesis_transaction.hash_hex()

with open("genesisprivatekey.pem", "r") as f:
	key = RSA.import_key(f.read())
	genesis_transaction.signature = pss.new(key).sign(genesis_transaction.hash_transaction())
	genesis_transaction.save()

print("Creating Genesis Block...")
genesis_block = Block.objects.create(data=str(genesis_transaction),
									previous_hash="",
									nonce="",
									block_difficulty=0,
									block_producer=genesis_account)
genesis_block.block_hash = genesis_block.hash_hex()
genesis_block.save()

print("Blockchain Genesis started!")