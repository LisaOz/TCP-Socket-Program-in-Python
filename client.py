import socket
import logging
import threading


# Configure logging
logging.basicConfig(filename='communication.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def run_client(client_id, server_ip, server_port, input_file):

    # Creating a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))

        with open(input_file, 'r') as file:  # read the messages from the input file
            messages = file.readlines()

            # Loop for multiple messages/users
            for message in messages:

                # Send the message to the server
                client_socket.sendall(message.encode('utf-8'))

                # Log the message
                logging.info(f"Client {client_id} sent to server ({server_ip}:{server_port}): {message.strip()}")

                # Receive response from server
                data = client_socket.recv(1024)
                print(f"Client {client_id} received from server: ", data.decode('utf-8'))

                # Log the server's response
                logging.info(f"Client {client_id} received from server ({server_ip}:{server_port}:{data.decode('utf-8')})")
    except Exception as e:
        print("Error sending/receiving message:", e)
        logging.error(f"Error sending/receiving message:, {e}")
    finally:
        # Close the socket
        client_socket.close()


def start_clients(num_clients, server_ip, server_port, input_file):

    threads = []  # list to keep track of the client threads that will be created

    for i in range(num_clients):
        #  Each iteration represents the creation and starting of a new client thread
        thread = threading.Thread(target=run_client, args=(i, server_ip, server_port, input_file))  # Creates a new thread object
        thread.start() # Starts the newly created thread
        threads.append(thread) # The newly started thread is added to the threads list to keep track of it.

    # The join() method called on each thread to make the main program wait until the thread has finished its execution.
    # so the main program doesn't exit before all client threads complete their tasks.
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    # Target IP address and port
    ip_address = '127.0.0.1'
    port = 5555

    # Input_file containing messages
    input_file = 'messages.txt'

    # Run the client
    start_clients(10, ip_address, port, input_file)
