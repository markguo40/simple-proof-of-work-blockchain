# All hash stored in unicode version of sha256 hexdigest. Length of 64
from django.db import models
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

# Book keeping for all Account (does not have to include private key)
class Account(models.Model):
	address = models.CharField(max_length=100)
	balance = models.DecimalField(max_digits=28, decimal_places=18, default=0)
	current_nonce = models.BigIntegerField(default=0)

	def __str__(self):
		return self.address

class Block(models.Model):
	data = models.TextField(default="")
	previous_hash = models.CharField(max_length=100)
	nonce = models.CharField(max_length=100, default="")
	block_difficulty = models.IntegerField()
	block_hash = models.CharField(max_length=100, blank=True) #Input after block creation
	block_producer = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)

	def hash_block(self):
		# return sha256 object
		sha = SHA256.new()
		sha.update(bytes(str(self.pk) + \
						str(self.data) + \
						str(self.previous_hash) + \
						str(self.nonce) +\
						str(self.block_difficulty) + 
						str(self.block_producer.address), 'utf-8'))
		return sha

	def hash_hex(self):
		return self.hash_block().hexdigest()

	def __str__(self):
		return self.block_hash

class Transaction(models.Model):
	receiver = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="receive")
	amount = models.DecimalField(max_digits=28, decimal_places=18, default=0)
	signature = models.BinaryField(max_length=1000000, blank=True)
	sender = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="send")
	nonce = models.BigIntegerField()
	transaction_hash = models.CharField(max_length=100, blank=True) #Input after transaction creation

	def hash_transaction(self):
		# return sha256 object
		sha = SHA256.new()
		sha.update(bytes(str(self.receiver.address) + \
						str(self.amount) + \
						str(self.sender.address) +\
						str(self.nonce), 'utf-8'))
		return sha

	def hash_hex(self):
		return self.hash_transaction().hexdigest()

	def __str__(self):
		return self.transaction_hash


