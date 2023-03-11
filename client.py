import pickle
import socket

# Client component
class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_request(self, transaction):
        # Serialize transaction object
        data = pickle.dumps(transaction)

        # Connect to server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            # Send data to server
            s.sendall(data)

            # Receive response from server
            response_data = s.recv(1024)

        # Deserialize response object
        response = pickle.loads(response_data)

        return response