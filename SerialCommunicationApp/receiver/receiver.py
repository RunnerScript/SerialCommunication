import tkinter as tk
from tkinter import ttk
import serial
import time
from database import DatabaseHandler

class ConnectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect to Serial Port")
        self.root.geometry("400x200")

        # Label for Serial Port input
        self.port_label = tk.Label(self.root, text="Enter Serial Port (e.g., COM3, /dev/ttyUSB0):")
        self.port_label.pack(pady=10)

        # Input field for Serial Port
        self.port_input = tk.Entry(self.root, width=40)
        self.port_input.pack(pady=10)

        # Connect button
        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect_to_port)
        self.connect_button.pack(pady=10)

        # Status label for connection status
        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.pack(pady=5)

    def connect_to_port(self):
        """Try connecting to the entered serial port."""
        port = self.port_input.get().strip()
        if not port:
            self.status_label.config(text="Please enter a valid serial port.", fg="red")
            return

        # Try to open the serial connection
        try:
            self.ser = serial.Serial(port, 9600, timeout=1)  # Adjust baud rate if needed
            self.status_label.config(text=f"Connected to {port}", fg="green")
            self.root.after(1000, self.show_receiver_ui)  # Delay to ensure the connection is made
        except serial.SerialException:
            self.status_label.config(text=f"Failed to connect to {port}", fg="red")

    def show_receiver_ui(self):
        """Show the receiver UI after successful connection."""
        self.root.destroy()  # Close the connection screen
        self.receiver_window()

    def receiver_window(self):
        """Create and show the main receiver window."""
        self.root = tk.Tk()  # New root window for receiver UI
        self.app = ReceiverApp(self.root, self.ser)  # Pass serial connection to ReceiverApp
        self.root.mainloop()


class ReceiverApp:
    def __init__(self, root, ser):
        self.root = root
        self.ser = ser  # Serial connection passed from ConnectionApp
        self.root.title("Receiver Application")
        self.root.geometry("500x400")

        # Store messages and timestamps
        self.messages = []

        # Create a scrollable canvas for displaying received messages
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.message_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.message_frame, anchor="nw")

        # Status label for showing message reception status
        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.pack(pady=10)

        # Initialize the database handler
        self.db_handler = DatabaseHandler()

        # Start receiving messages
        self.receive_messages()

    def receive_messages(self):
        """Periodically check for new messages from the serial port."""
        try:
            if self.ser.in_waiting > 0:
                raw_message = self.ser.readline().decode("utf-8", errors="ignore").strip()
                
                if raw_message:
                    self.handle_message(raw_message)

            # Remove old messages (older than 10 minutes)
            self.remove_old_messages()
            
            self.root.after(100, self.receive_messages)  # Check for new messages every 100ms
        except serial.SerialException as e:
            self.status_label.config(text=f"Error: {e}", fg="red")

    def handle_message(self, raw_message):
        """Parse and process incoming messages."""
        try:
            # Example message format: "Hello World|Medium|Left-to-Right"
            
            all_messages = raw_message.split('___')
            for msg in all_messages:
                if msg:
                    message, speed, style = msg.split('|')
                    timestamp = time.time()  # Get current time in seconds
                    self.messages.append((message, speed, style, timestamp))

                    # Save to database
                    self.db_handler.save_message(raw_message)

            # Display messages iteratively
            self.animate_messages()

        except ValueError:
            self.status_label.config(text="Received message format is invalid.", fg="red")

    def remove_old_messages(self):
        """Remove messages that have been displayed for more than 10 minutes."""
        current_time = time.time()
        self.messages = [(msg, speed, style, timestamp)
                         for msg, speed, style, timestamp in self.messages
                         if current_time - timestamp < 600]  # 600 seconds = 10 minutes

        # Update the UI by removing old messages
        self.display_messages()

    def display_messages(self):
        """Display received message on the UI."""
        # Clear the old messages first
        for widget in self.message_frame.winfo_children():
            widget.destroy()

        # Display all messages
        for message in self.messages:
            message_label = tk.Label(self.message_frame, text=message[0], anchor="w", width=50, bg="white", fg="black")
            message_label.pack(pady=5)

            # Update the canvas scroll region
            self.canvas.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def animate_messages(self):
        """Iteratively display each message with a delay."""
        self.iterate_messages()

    def iterate_messages(self):
        """Iterate over messages with a delay to animate display."""
        if not self.messages:
            return  # If no messages to display, stop

        for index, message in enumerate(self.messages):
            message_label = tk.Label(self.message_frame, text=message[0], anchor="w", width=50, bg="white", fg="black")
            message_label.pack(pady=5)

            # Delay before displaying the next message
            self.root.after(index * 1000, self.update_message_display, message_label)

        # Update the canvas scroll region
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def update_message_display(self, message_label):
        """Update the display of each message."""
        if message_label.winfo_exists():  # Check if the widget exists before updating
            message_label.config(bg="lightgray")  # Change the background color after displaying

    def on_closing(self):
        """Handle the closing event."""
        print("Closing application...")
        self.ser.close()  # Close serial port
        self.db_handler.close()  # Close the database connection
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectionApp(root)  # Start with the connection screen
    root.mainloop()
