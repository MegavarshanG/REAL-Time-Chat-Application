import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

# Client setup
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_ip = '192.168.137.1'  # Replace with the server's IP address
port = 55555
server_address = (server_ip, port)

# GUI Class
class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")
       
        # Scrollable text area for displaying messages
        self.chat_area = scrolledtext.ScrolledText(root, state='disabled', wrap='word')
        self.chat_area.grid(row=0, column=0, columnspan=2)
       
        # Entry field for typing messages
        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.grid(row=1, column=0)
        self.message_entry.bind("<Return>", self.write_message)  # Bind Enter key to send message
       
        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.write_message)
        self.send_button.grid(row=1, column=1)
       
        # Initial nickname dialog
        self.nickname = simpledialog.askstring("Nickname", "Choose your nickname", parent=root)
       
        # Send join message to the server
        client.sendto(f"{self.nickname} joined!".encode('ascii'), server_address)
       
        # Start receiving thread
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def receive(self):
        while True:
            try:
                # Continuously listen for messages from the server
                message, _ = client.recvfrom(1024)
                self.display_message(message.decode('ascii'))
            except Exception as e:
                self.display_message("An error occurred!")
                break

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert('end', f"{message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview('end')  # Scroll to the latest message

    def write_message(self, event=None):
        message = self.message_entry.get()
        if message:
            # Display sent message in the client's chat area
            self.display_message(f"{self.nickname}: {message}")
            # Send message to the server
            client.sendto(f"{self.nickname}: {message}".encode('ascii'), server_address)
            self.message_entry.delete(0, 'end')

# Start the GUI
root = tk.Tk()
gui = ChatClientGUI(root)
root.mainloop()
