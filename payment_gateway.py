import hashlib
import json
from datetime import datetime


class PaymentGateway:
    def __init__(self):
        self.customers = {}
        self.merchants = {}
        self.products = {}
        self.transactions = []

    def add_customer(self, customer):
        self.customers[customer['id']] = customer

    def add_merchant(self, merchant):
        self.merchants[merchant['id']] = merchant

    def add_product(self, product):
        self.products[product['id']] = product

    def create_transaction(self, customer_id, merchant_id, product_id):
        customer = self.customers.get(customer_id)
        merchant = self.merchants.get(merchant_id)
        product = self.products.get(product_id)

        if not customer:
            return {"status": "error", "message": "Customer not found"}

        if not merchant:
            return {"status": "error", "message": "Merchant not found"}

        if not product:
            return {"status": "error", "message": "Product not found"}

        # Check if customer has enough funds
        if customer['balance'] < product['price']:
            return {"status": "error", "message": "Insufficient funds"}

        # Generate transaction ID
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        transaction_id = f"{customer_id}-{merchant_id}-{product_id}-{timestamp}"

        # Create transaction
        transaction = {
            "id": transaction_id,
            "customer_id": customer_id,
            "merchant_id": merchant_id,
            "product_id": product_id,
            "amount": product['price'],
            "timestamp": timestamp
        }

        # Add transaction to list
        self.transactions.append(transaction)

        # Update customer balance
        customer['balance'] -= product['price']

        # Update merchant balance
        merchant['balance'] += product['price']

        return {"status": "success", "message": "Transaction successful", "transaction_id": transaction_id}

    def verify_transaction(self, transaction_id):
        # Check if transaction ID is valid
        transaction = next((t for t in self.transactions if t['id'] == transaction_id), None)

        if not transaction:
            return {"status": "error", "message": "Transaction not found"}

        # Check if transaction has already been redeemed by merchant
        if transaction['redeemed']:
            return {"status": "error", "message": "Transaction has already been redeemed"}

        # Redeem transaction
        transaction['redeemed'] = True

        return {"status": "success", "message": "Transaction verified"}

    def sign(self, data):
        # Serialize data to JSON string
        json_data = json.dumps(data)

        # Hash the JSON string
        hashed_data = hashlib.sha256(json_data.encode('utf-8')).hexdigest()

        # Return the hash
        return hashed_data


# Create a PaymentGateway object
pg = PaymentGateway()

# Load customers from file
with open('data/customers.json') as f:
    customers_data = json.load(f)

for customer in customers_data:
    pg.add_customer(customer)

# Load merchants from file
with open('./data/merchants.json') as f:
    merchants_data = json.load(f)

for merchant in merchants_data:
    pg.add_merchant(merchant)

# Load products from file
with open('./data/products.json') as f:
    products_data = json.load(f)

for product in products_data:
    pg.add_product(product)

