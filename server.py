import payment_gateway
import socket
import pickle
import json
import os
import base64
from Crypto.Cipher import AES
import AESkey
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Server component
class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        # Listen for incoming connections
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
                
            while True:
                print("Waiting for client connection...")
                conn, addr = s.accept()
                with conn:
                    print(f"Client {addr[0]}:{addr[1]} connected")

                    # Receive data from client
                    data = conn.recv(1024)
                    response_data = {}
                    if not data:
                        continue
    
                    AESkey = base64.b64decode(os.environ.get('AESkey'))
                    with open('./data/private_key.pem', 'rb') as f:
                        private_key = RSA.import_key(f.read())
                    data = base64.b64decode(pickle.loads(data))

                       
                    cipherKPM = PKCS1_OAEP.new(private_key)
                    data = cipherKPM.decrypt(data)

                    nonce = data[:16]
                    tag = data[16: 32]
                    ciphertext = data[32:]
                    cipher = AES.new(AESkey, AES.MODE_EAX, nonce)
                    result = cipher.decrypt_and_verify(ciphertext, tag)

                    Customer_Pubk_file = pickle.loads(result)
                    print(Customer_Pubk_file)

                    with open(str(Customer_Pubk_file)[2:-1], 'rb') as f:
                         public_keyC = RSA.import_key(f.read())

                    
                    cipherKPubC = PKCS1_OAEP.new(public_keyC)

                    with open('./data/private_key.pem', 'rb') as f:
                        private_key = RSA.import_key(f.read())

                    
                    cipherKPrvM = PKCS1_OAEP.new(private_key)
                        
                    sid = random.randint(10**9, 10**10-1)
                    plain_text = str(sid)

                    hash_object = SHA256.new(plain_text.encode())
                    signature = pkcs1_15.new(private_key).sign(hash_object)

                    data = {'sid':cipherKPubC.encrypt(plain_text.encode()).hex(), 'signature': signature}
                    serialized_data = pickle.dumps(data)
                    response_data =  serialized_data
                    authenticated = True
                    # Send response to client
                    conn.sendall(response_data)

                   #after 
                    data = conn.recv(1024)
                    # Deserialize transaction object
                    transaction = pickle.loads(data)

                    # Process transaction
                    success = payment_gateway.get_payment_gateway().create_transaction(transaction["customer_id"], transaction["merchant_id"],
                                                         transaction["product_id"], transaction["quantity"])
                    # Create response object
                    response = {"result": success}

                    # Serialize response object
                    response_data = pickle.dumps(response)
                    conn.sendall(response_data)

                        
                       
   
    def share_key(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        with open('./data/private_key.pem', 'wb') as f:
            f.write(private_key)

        with open('./data/public_key.pem', 'wb') as f:
            f.write(public_key)

if __name__ == "__main__":
    # Create server object
    server = Server("localhost", 12345)
    server.share_key()
    # Run server
    server.run()
