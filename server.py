import payment_gateway
import socket
import pickle


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

                    if not data:
                        continue

                    # Deserialize transaction object
                    transaction = pickle.loads(data)

                    # Process transaction
                    success = payment_gateway.get_payment_gateway().create_transaction(transaction["customer_id"], transaction["merchant_id"],
                                                         transaction["product_id"], transaction["quantity"])

                    # Create response object
                    response = {"result": success}

                    # Serialize response object
                    response_data = pickle.dumps(response)

                    # Send response to client
                    conn.sendall(response_data)


if __name__ == "__main__":
    # Create server object
    server = Server("localhost", 12345)

    # Run server
    server.run()
