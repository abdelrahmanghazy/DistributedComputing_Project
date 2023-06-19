import socket
import threading

class ChatClient:
    """
    This class represents a chat client.

    Attributes:
        nickname: The client's nickname.
        client: The socket object that is used to connect to the server.

    Methods:
        receive_messages: Receives messages from the server.
        send_messages: Sends messages to the server.
        start: Starts the client.
    """

    def __init__(self, host, port):
        """
        Initializes the client.

        Args:
            host: The hostname of the server.
            port: The port of the server.
        """
        self.nickname = input("Choose your nickname: ")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def receive_messages(self):
        """
        Receives messages from the server.

        This method runs in a separate thread and continuously receives messages from the server.
        """
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                print(message)
            except:
                print("An error occurred while receiving messages.")
                self.client.close()
                break

    def send_messages(self):
        """
        Sends messages to the server.

        This method runs in a separate thread and continuously sends messages to the server.
        """
        while True:
            message = input('')
            if message.lower() == 'quit':
                self.client.send('quit'.encode('utf-8'))
                self.client.close()
                break
            else:
                full_message = '{}: {}'.format(self.nickname, message)
                self.client.send(full_message.encode('utf-8'))

    def start(self):
        """
        Starts the client.

        This method starts the two threads that receive and send messages.
        """
        receive_thread = threading.Thread(target=self.receive_messages)
        send_thread = threading.Thread(target=self.send_messages)

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()
