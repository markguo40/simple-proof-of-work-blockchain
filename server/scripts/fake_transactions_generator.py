from Crypto.PublicKey import RSA
from server.models import Block, Account, Transaction
from blockchain.settings import GENESIS_ADDRESS, MAX_TX_PER_BLOCK
from Crypto.Signature import pss
from decimal import Decimal
from Crypto.Random import random

# These are fake addresses, I do not have their private key
account_addresses = ["3a50a6f79f59cf53791d8f6611558f0e22487d263072bc5cfa155fef59f73bad",
					"abe85bae3d405821e09aae62e109fe5e4d8bf1768b875c96ef961c4e4f762298",
					"c4c894d86b669eb49d357eda8790ad260fa0e3429fb287f1f2fecc3c0b25d733",
					"91649485f55f3f120b50a92b51fbebab566547fc78b85687e2f725fe663e5526",
					"3a50a6f79f59cf53791d8f6611558f0e22487d263072bc5cfa155fef59f73bad",
					"0e3f5e572d4bb8db91f225a52b647d79c827da64c364f3a80b2d6812f82454bc",
					"185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969"]

def setup_fake_accounts():
	# it will do nothing if these accounts are already created
	for address in account_addresses:
		account, created = Account.objects.get_or_create(address=address)
		account.save()

def generate_fake_generations():
	genesis_account = Account.objects.get(address=GENESIS_ADDRESS)
	num_transactions = random.randint(1, MAX_TX_PER_BLOCK)

	with open("genesisprivatekey.pem", "r") as f:
		key = RSA.import_key(f.read())

	transactions = []
	print("there are " + str(num_transactions) + "transactions generated in this block")
	for _ in range(num_transactions):
		amount = Decimal(str(random.randint(0, 10)))
		target_address = random.choice(account_addresses)
		target_account = Account.objects.get(address=target_address)

		genesis_transactions = Transaction.objects.filter(sender=genesis_account)
		nonce = len(genesis_transactions) + 1
		transaction = Transaction.objects.create(sender=genesis_account, 
														amount=amount,
														receiver=target_account,
														nonce=nonce)
		transaction.transaction_hash = transaction.hash_hex()
		transaction.signature = pss.new(key).sign(transaction.hash_transaction())
		transaction.save()
		transactions.append(transaction)

	return transactions

def process_transactions(transactions):
	for transaction in transactions:
		amount = transaction.amount
		sender = transaction.sender
		receiver = transaction.receiver
		sender.balance -= amount
		receiver.balance += amount
		sender.save()
		receiver.save()

def pack_transactions_to_str(transactions):
	result = ""
	for transaction in transactions:
		result += str(transaction) + "|"
	return result.strip("|")