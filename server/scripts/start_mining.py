from blockchain.settings import BLOCK_AWARD, BLOCK_DIFFICULTY, TESTING, MINER_ADDRESS
from Crypto.Hash import SHA256
from Crypto.Random import random
from server.models import Block, Account
from decimal import Decimal
import server.scripts.fake_transactions_generator as tx_generator
import time

SELECTION = '0123456789abcdefghijklnmopqrstuvwxyz'

tx_generator.setup_fake_accounts()

miner_account = Account.objects.get(address=MINER_ADDRESS)

h = SHA256.new()
while True:
	# Proof of Work mining implementation
	selected = random.choice(SELECTION)
	bytes_selected = bytes(selected, "utf-8")

	h.update(bytes_selected)
	nonce = h.hexdigest()

	tested_nonce = nonce[:BLOCK_DIFFICULTY]
	if tested_nonce == ("0" * BLOCK_DIFFICULTY):
		transactions = tx_generator.generate_fake_generations()
		tx_generator.process_transactions(transactions)
		data = tx_generator.pack_transactions_to_str(transactions)

		lastblock = Block.objects.all().last()

		block = Block.objects.create(data=data,
									previous_hash=lastblock.block_hash,
									nonce=nonce,
									block_difficulty=BLOCK_DIFFICULTY,
									block_producer=miner_account)
		block.block_hash = block.hash_hex()

		# miner receiving block reward
		miner_account.balance += Decimal(str(BLOCK_AWARD))
		miner_account.save()
		block.save()

		print("Block " + str(block.pk) + " hash: " + block.block_hash + " created")
		if TESTING:
			print("Sleeping before restart mining......")
			# If it is testing mode, every block produced will sleep 10 second to prevent overheating CPU
			time.sleep(10)

		h = SHA256.new()

