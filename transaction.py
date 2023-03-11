import hashlib
import hmac

class Transaction:
    def __init__(self, customer_key, merchant_key, amount, message, signature):
        self.customer_key = customer_key
        self.merchant_key = merchant_key
        self.amount = amount
        self.message = message
        self.signature = signature

    def sign(self, key):
        h = hmac.new(key.encode(), self.message.encode(), hashlib.sha256)
        self.signature = h.hexdigest()

    def verify_signature(self):
        h = hmac.new(self.merchant_key.encode(), self.message.encode(), hashlib.sha256)
        return h.hexdigest() == self.signature