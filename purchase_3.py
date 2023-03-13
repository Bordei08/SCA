# Import necessary modules
import pickle
import socket
import payment_gateway
import json
import base64
import os
from Crypto.Cipher import AES
import AESkey
import rsa
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

# Connect to server
s = socket.socket()
host = "localhost"
port = 12345
s.connect((host, port))


AESkey = base64.b64decode(os.environ.get('AESkey'))
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()
with open('./data/private_keyC.pem', 'wb') as f:
    f.write(private_key)

with open('./data/public_keyC.pem', 'wb') as f:
     f.write(public_key)    

with open('./data/public_key.pem', 'rb') as f:
    pem_public_key = f.read()

publickeyM = RSA.import_key(pem_public_key)
cipherKPubM = PKCS1_OAEP.new(publickeyM)

data  = pickle.dumps(b'./data/public_keyC.pem')
cipher = AES.new(AESkey, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)
nonce = cipher.nonce

msg = nonce + tag + ciphertext

msg = cipherKPubM.encrypt(msg)


s.send(pickle.dumps(base64.b64encode(msg).decode('utf-8')))

response = s.recv(1024)
received_data = pickle.loads(response)


with open('./data/private_keyC.pem',  'rb') as f:
    pem_private_key = f.read()
private_key = RSA.import_key(pem_private_key)
cipherKPrvC = PKCS1_OAEP.new(private_key)

sid = cipherKPrvC.decrypt(bytes.fromhex(received_data['sid'])).decode()


hash_object = SHA256.new(sid.encode())


signature = received_data['signature']


with open('./data/public_key.pem', 'rb') as f:
    pem_public_key = f.read()

publickeyM = RSA.import_key(pem_public_key)

try:
    pkcs1_15.new(publickeyM ).verify(hash_object, signature)
    print("The signature is valid.")
except (ValueError, TypeError):
    print("The signature is invalid.")

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

# POS accidentally sends the same transaction twice because of network issues/POS malfunction

# Connect to server
s = socket.socket()
host = "localhost"
port = 12345
s.connect((host, port))



AESkey = base64.b64decode(os.environ.get('AESkey'))
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()
with open('./data/private_keyC.pem', 'wb') as f:
    f.write(private_key)

with open('./data/public_keyC.pem', 'wb') as f:
     f.write(public_key)    

with open('./data/public_key.pem', 'rb') as f:
    pem_public_key = f.read()

publickeyM = RSA.import_key(pem_public_key)
cipherKPubM = PKCS1_OAEP.new(publickeyM)

data  = pickle.dumps(b'./data/public_keyC.pem')
cipher = AES.new(AESkey, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)
nonce = cipher.nonce

msg = nonce + tag + ciphertext

msg = cipherKPubM.encrypt(msg)


s.send(pickle.dumps(base64.b64encode(msg).decode('utf-8')))

response = s.recv(1024)
received_data = pickle.loads(response)


with open('./data/private_keyC.pem',  'rb') as f:
    pem_private_key = f.read()
private_key = RSA.import_key(pem_private_key)
cipherKPrvC = PKCS1_OAEP.new(private_key)

sid = cipherKPrvC.decrypt(bytes.fromhex(received_data['sid'])).decode()


hash_object = SHA256.new(sid.encode())


signature = received_data['signature']


with open('./data/public_key.pem', 'rb') as f:
    pem_public_key = f.read()

publickeyM = RSA.import_key(pem_public_key)

try:
    pkcs1_15.new(publickeyM ).verify(hash_object, signature)
    print("The signature is valid.")
except (ValueError, TypeError):
    print("The signature is invalid.")


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
    receipt = payment_gateway.get_payment_gateway().generate_receipt(response_data["result"]["transaction_id"])

    # check for fake receipt
    if receipt["status"] == "error":
        print("Error:", receipt["message"])
    else:
        print("Transaction successful. Receipt:", receipt)

else:
    print("Transaction failed. Reason:", response_data['result']["message"])

# Close connection

s.close()

# Output: Transaction failed. Reason: Transaction already processed
