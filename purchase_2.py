# Import necessary modules
import pickle
import socket
import payment_gateway

# Connect to server
s = socket.socket()
host = "localhost"
port = 12345
s.connect((host, port))

# Send transaction request to server
request = {
    "customer_id": "customer2",
    "merchant_id": "merchant2",
    "product_id": "product2",
    "quantity": 1
}

# send pickled data
s.send(pickle.dumps(request))

# Receive response from server
response = s.recv(1024)

# deserialize response
response_data = pickle.loads(response)

# Check if response is valid
if response_data["result"]["status"] == "success":
    # Get digital receipt from payment gateway
    receipt = payment_gateway.get_payment_gateway().generate_receipt(response_data["result"]["transaction_id"])

    # check for fake receipt
    if receipt["receipt"]["customer"]['id'] != request["customer_id"] or receipt["receipt"]["merchant"]['id'] != request["merchant_id"] or \
            receipt["receipt"]["product"]['id'] != request["product_id"] or receipt["receipt"]["quantity"] != request["quantity"]:
        print("Error: Fake receipt")
    elif receipt["status"] == "error":
        print("Error:", receipt["message"])
    else:
        print("Transaction successful. Receipt:", receipt)

else:
    print("Transaction failed. Reason:", response_data['result']["message"])

# Close connection
s.close()

# Output: Transaction failed. Reason: Insufficient funds