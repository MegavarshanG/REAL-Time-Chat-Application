import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Server setup
host = '0.0.0.0'  # Bind to all available interfaces
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host, port))

clients = set()  # Using a set to store client addresses

# GUI Class
class ChatServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Server")
        
        # Scrollable text area for displaying messages
        self.chat_area = scrolledtext.ScrolledText(root, state='disabled', wrap='word')
        self.chat_area.grid(row=0, column=0, columnspan=2)
        
        # Button to start the server
        self.start_button = tk.Button(root, text="Start Server", command=self.start_server)
        self.start_button.grid(row=1, column=0, columnspan=2)
        
        # Log area for server information
        self.log_area = scrolledtext.ScrolledText(root, state='disabled', wrap='word', height=10)
        self.log_area.grid(row=2, column=0, columnspan=2)

    def start_server(self):
        self.start_button.config(state='disabled')
        self.display_log(f"Server started and listening on {host}:{port}")
        thread = threading.Thread(target=self.receive)
        thread.start()

    def broadcast(self, message, client_address):
        # Broadcast message to all clients except the sender
        for client in clients:
            if client != client_address:
                server.sendto(message, client)

    def receive(self):
        while True:
            try:
                message, client_address = server.recvfrom(1024)
                message = message.decode('ascii')
                
                # Check if client is joining for the first time
                if message.endswith("joined!"):
                    clients.add(client_address)
                    self.display_message(f"{message}")
                    self.display_log(f"Client {client_address} joined the chat.")
                else:
                    self.broadcast(message.encode('ascii'), client_address)
                    self.display_message(message)
            except Exception as e:
                self.display_log(f"Error receiving message: {e}")

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert('end', f"{message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview('end')

    def display_log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert('end', f"{message}\n")
        self.log_area.config(state='disabled')
        self.log_area.yview('end')

# Start the GUI
root = tk.Tk()
server_gui = ChatServerGUI(root)
root.mainloop()
