import socket
from ecdsa import SigningKey


## pip install ecdsa (pentru Signingkey)
'''
private_key = SigningKey.generate() # uses NIST192p
signature = private_key.sign(b"Educative authorizes this shot")
print(signature)
'''
def get_public_key():
    return private_key.verifying_key

def put_signature(msg):
    return private_key.sig(msg)

def start_customer():
    ClientSocket = socket.socket()
    host = '127.0.0.1'
    port = 1233

    print('Waiting for connection')
    try:
        ClientSocket.connect((host, port))
    except socket.error as e:
        print(str(e))

    Response = ClientSocket.recv(1024)
    while True:
        Input = input('Say Something: ')
        ClientSocket.send(str.encode(Input))
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))

    ClientSocket.close()


start_customer()    