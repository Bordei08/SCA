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
    "customer_id": "customer1",
    "merchant_id": "merchant1",
    "product_id": "product1",
    "quantity": 2
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
    print("Transaction successful.")
else:
    print("Transaction failed. Reason:", response_data["message"])

# Close connection
s.close()
