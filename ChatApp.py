import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import os
import sys

# ==========================
# SERVER CODE
# ==========================
class ChatServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = []

        print(f"🔵 Server started on {host}:{port}")
        self.accept_connections()

    def broadcast(self, message, _client):
        """Send message to all connected clients except the sender."""
        for client in self.clients:
            if client != _client:
                try:
                    client.send(message)
                except:
                    self.clients.remove(client)

    def handle_client(self, client, address):
        """Handle messages from a single client."""
        print(f"🟢 New connection: {address}")
        while True:
            try:
                message = client.recv(1024)
                if message:
                    print(f"[{address}] {message.decode('utf-8')}")
                    self.broadcast(message, client)
                else:
                    break
            except:
                break
        print(f"🔴 Connection closed: {address}")
        self.clients.remove(client)
        client.close()

    def accept_connections(self):
        """Accept new client connections."""
        print("🟡 Waiting for connections...")
        while True:
            client, address = self.server.accept()
            self.clients.append(client)
            threading.Thread(target=self.handle_client, args=(client, address)).start()

# ==========================
# CLIENT CODE
# ==========================
class ChatClient:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

        self.gui_running = False
        self.running = True

        gui_thread = threading.Thread(target=self.start_gui)
        gui_thread.start()

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def start_gui(self):
        """Create and launch the client GUI."""
        self.root = tk.Tk()
        self.root.title("Python Chat Application")

        # Message display area
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, bg="#f4f4f4", fg="#333333", font=("Arial", 12))
        self.text_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        self.text_area.config(state="disabled")

        # Message input field
        self.input_field = tk.Entry(self.root, bg="white", fg="black", font=("Arial", 12))
        self.input_field.pack(padx=10, pady=10, fill=tk.X)
        self.input_field.bind("<Return>", self.send_message)

        # Exit button
        self.exit_button = tk.Button(self.root, text="Exit", command=self.close_connection, bg="#ff4d4d", fg="white", font=("Arial", 12))
        self.exit_button.pack(padx=10, pady=10)

        self.gui_running = True
        self.root.protocol("WM_DELETE_WINDOW", self.close_connection)
        self.root.mainloop()

    def receive_messages(self):
        """Continuously receive messages from the server."""
        while self.running:
            try:
                message = self.client.recv(1024).decode("utf-8")
                if message:
                    self.display_message(message)
            except:
                break

    def display_message(self, message):
        """Display received message in the text area."""
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state="disabled")
        self.text_area.yview(tk.END)

    def send_message(self, event=None):
        """Send message to the server."""
        message = self.input_field.get()
        if message:
            self.client.send(message.encode("utf-8"))
            self.input_field.delete(0, tk.END)

    def close_connection(self):
        """Gracefully close the connection."""
        self.running = False
        self.client.close()
        self.root.destroy()
        print("🔴 Disconnected from server.")

# ==========================
# MAIN FUNCTION
# ==========================
def main():
    print("Welcome to Python Chat Application")
    print("1. Start Server")
    print("2. Start Client")

    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        # Start Server
        print("\nStarting Server...\n")
        ChatServer()
    elif choice == "2":
        # Start Client
        print("\nStarting Client...\n")
        host = input("Enter Server IP (default 127.0.0.1): ").strip() or "127.0.0.1"
        port = int(input("Enter Server Port (default 12345): ").strip() or 12345)
        try:
            ChatClient(host, port)
        except Exception as e:
            print(f"❌ Unable to connect to server: {e}")
    else:
        print("Invalid choice. Please enter 1 or 2.")
        sys.exit()

if __name__ == "__main__":
    main()
