import tkinter as tk
from tkinter import messagebox
import serial
import sqlite3

class TransmitterApp:
    def __init__(self, root,port,baud_rate):
        """Intialize Application """
        self.root = root
        self.root.title("Transmitter")
        # DB setup
        self.conn = sqlite3.connect('messages.db')
        self.cursor = self.conn.cursor()
        self.create_database()

        # Set up serial communication parameters
        self.serial_port = port
        self.baud_rate = baud_rate

        # create GUI
        self.create_widgets()

    def create_database(self):
        """create Table if not exists and add  sample messages to table"""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, message TEXT)")
        self.cursor.execute("SELECT id, message FROM messages");
        messages = self.cursor.fetchall()
        if len(messages)<1:
            self.cursor.execute("INSERT INTO messages (message) VALUES ('Sample message 1'), ('Sample message 2')")
        self.conn.commit()

    def create_widgets(self):
        """Create all the UI elements such as buttons, labels, and input fields"""
        # Label for message input
        self.message_label = tk.Label(self.root, text="Enter Message:")
        self.message_label.pack(padx=10, pady=5)

        # Input field for the message
        self.message_text = tk.Entry(self.root, width=60, font=('Arial', 14))
        self.message_text.pack(padx=10, pady=5)

        # Get messages from the database to show in the dropdown
        self.cursor.execute("SELECT id, message FROM messages")
        messages = self.cursor.fetchall()

        # Create a dictionary and list to populate the dropdown
        self.messages_dict = {str(msg[0]): msg[1] for msg in messages}
        message_options = [msg[1] for msg in messages]

        # Dropdown menu for selecting a message from the database
        self.message_db = tk.StringVar(self.root)
        self.dropdown = tk.OptionMenu(self.root, self.message_db, *message_options, command=self.on_message_select)
        self.dropdown.pack(padx=10, pady=5)

        # Button to send the message
        self.send_button = tk.Button(self.root, text="Send Message", command=self.send_message)
        self.send_button.pack(padx=10, pady=5)

        # Status label to show whether the message was sent successfully
        self.status_label = tk.Label(self.root, text="Status: Idle", fg="blue")
        self.status_label.pack(padx=10, pady=5)

        # Button to load a message from the database
        self.load_button = tk.Button(self.root, text="Load Message from DB", command=self.load_message_from_db)
        self.load_button.pack(padx=10, pady=5)

    def on_message_select(self, selected_message):
        """Update the input field with the selected message from the dropdown"""
        self.message_text.delete(0, tk.END)  # Clear the input field
        self.message_text.insert(0, selected_message)  # Insert the selected message

    def send_message(self):
        """Send the message over the serial port"""
        message = self.message_text.get()  # Get the text from the input field
        if message:  # If there is a message to send
            try:
                # Send the message via the serial port (COM2 at 9600 baud rate)
                with serial.Serial(self.serial_port, self.baud_rate, timeout=1) as ser:
                    ser.write(message.encode('utf-8'))
                # Update status label to show message was sent successfully
                self.status_label.config(text="Message sent successfully", fg="green")
            except Exception as e:
                # If an error occurs, show the error message in the status label
                self.status_label.config(text=f"Error: {e}", fg="red")
        else:
            # Show a warning if no message is entered
            messagebox.showwarning("Input Error", "Please enter a message to send.")

    def load_message_from_db(self):
        """Load the selected message from the database into the input field"""
        selected_message = self.message_db.get()  # Get the selected message from the dropdown
        self.cursor.execute("SELECT message FROM messages WHERE message=?", (selected_message,))
        msg = self.cursor.fetchone()
        self.message_text.delete(0, tk.END)  # Clear the input field
        self.message_text.insert(0, msg[0] if msg else "")  # Insert the selected message

    def close_database(self):
        """Close the database connection when the app is closed"""
        self.conn.close()


if __name__ == "__main__":
    port = input("Enter transmitter port")
    root = tk.Tk()
    baud_rate = 9600
    app = TransmitterApp(root,port,baud_rate)
    root.mainloop()
    app.close_database()
