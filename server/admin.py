from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

class AccountAdmin(admin.ModelAdmin):
    list_display = ("address", "balance", "current_nonce", )


class BlockAdmin(admin.ModelAdmin):
    list_display = ("previous_hash", "nonce", "block_difficulty", "block_hash", "block_producer",)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("receiver", "amount", "signature", "sender", "nonce", "transaction_hash", )

admin.site.register(Account, AccountAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Transaction, TransactionAdmin)