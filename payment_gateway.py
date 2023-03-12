import hashlib
import json
import time


class PaymentGateway:
    def __init__(self):
        self.customers = {}
        self.merchants = {}
        self.products = {}

    def add_customer(self, customer):
        self.customers[customer['id']] = customer

    def add_merchant(self, merchant):
        self.merchants[merchant['id']] = merchant

    def add_product(self, product):
        self.products[product['id']] = product

    def create_transaction(self, customer_id, merchant_id, product_id, quantity):
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
        if customer['balance'] < product['price'] * quantity:
            return {"status": "error", "message": "Insufficient funds"}

        # Generate transaction ID
        timestamp = int(time.time())
        transaction_id = f"{customer_id}-{merchant_id}-{product_id}-{timestamp}"

        # Create transaction
        transaction = {
            "id": transaction_id,
            "customer_id": customer_id,
            "merchant_id": merchant_id,
            "product_id": product_id,
            "quantity": quantity,
            "timestamp": timestamp,
            "redeemed": False
        }

        # Add transaction to transactions.json
        with open("transactions.json", "r") as f:
            # if file is empty the ValueError will be thrown
            try:
                transactions = json.load(f)
            except ValueError:
                transactions = []

        transactions.append(transaction)

        with open("transactions.json", "w") as f:
            json.dump(transactions, f)

        verification_result = self.verify_transaction(transaction_id)
        if verification_result['status'] != 'success':
            return verification_result

        # Update customer balance
        customer['balance'] -= product['price']

        # Update merchant balance
        merchant['balance'] += product['price']


        return {"status": "success", "message": "Transaction successful", "transaction_id": transaction_id}

    def verify_transaction(self, transaction_id):
        # Check if transaction ID is valid by checking if it exists in transactions.json
        with open("transactions.json", "r") as f:
            transactions = json.load(f)

        transaction = next((t for t in transactions if t['id'] == transaction_id), None)

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

    def generate_receipt(self, transaction_id):
        # Check if transaction ID is valid
        with open("transactions.json", "r") as f:
            transactions = json.load(f)

        # check if there's been a transaction with the same customer, merchant and product in the id within the last 3 seconds
        import re
        regex = re.compile(r'(.*)-(.*)-(.*)-(.*)')
        match = regex.match(transaction_id)
        customer_id = match.group(1)
        merchant_id = match.group(2)
        product_id = match.group(3)
        timestamp = match.group(4)

        # check if there is more than 1 transaction with the same id
        if len([t for t in transactions if t['customer_id'] == customer_id and t['merchant_id'] == merchant_id and t[
            'product_id'] == product_id and int(t['timestamp']) > int(timestamp) - 3]) > 1:
            return {"status": "error", "message": "Transaction has already been redeemed"}

        transaction = next((t for t in transactions if t['id'] == transaction_id), None)

        if not transaction:
            return {"status": "error", "message": "Transaction not found"}

        # Verify transaction
        verification_result = self.verify_transaction(transaction_id)
        if verification_result['status'] != 'success':
            return verification_result


        # Get customer and merchant details
        customer = self.customers.get(transaction['customer_id'])
        merchant = self.merchants.get(transaction['merchant_id'])
        product = self.products.get(transaction['product_id'])

        # Generate receipt
        receipt = {
            "customer": customer,
            "merchant": merchant,
            "product": product,
            "quantity": transaction['quantity'],
            "timestamp": transaction['timestamp']
        }

        return {"status": "success", "message": "Receipt generated", "receipt": receipt}


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



def get_payment_gateway():
    return pg

