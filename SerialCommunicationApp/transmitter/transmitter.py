import tkinter as tk
from tkinter import ttk, messagebox
import serial

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
            self.root.after(1000, self.show_transmitter_ui)  # Delay to ensure the connection is made
        except serial.SerialException:
            self.status_label.config(text=f"Failed to connect to {port}", fg="red")

    def show_transmitter_ui(self):
        """Show the transmitter UI after successful connection."""
        self.root.destroy()  # Close the connection screen
        self.transmitter_window()

    def transmitter_window(self):
        """Create and show the main transmitter window."""
        self.root = tk.Tk()  # New root window for transmitter UI
        self.app = TransmitterApp(self.root, self.ser)  # Pass serial connection to TransmitterApp
        self.root.mainloop()

class TransmitterApp:
    def __init__(self, root, ser):
        self.root = root
        self.ser = ser  # Serial connection passed from ConnectionApp
        self.root.title("Transmitter Application")
        self.root.geometry("400x300")

        # Message input field
        self.message_label = tk.Label(self.root, text="Enter Message:")
        self.message_label.pack(pady=5)
        self.message_input = tk.Entry(self.root, width=40)
        self.message_input.pack(pady=5)

        # Dropdown for selecting predefined messages from DB
        self.message_dropdown_label = tk.Label(self.root, text="Select Message from DB:")
        self.message_dropdown_label.pack(pady=5)
        self.message_dropdown = ttk.Combobox(self.root, values=["Message 1", "Message 2", "Message 3"], width=40)
        self.message_dropdown.pack(pady=5)
        self.message_dropdown.bind("<<ComboboxSelected>>", self.set_message_input)

        # Scrolling parameters (Speed and Style)
        self.scroll_params_label = tk.Label(self.root, text="Scrolling Parameters:")
        self.scroll_params_label.pack(pady=5)

        self.speed_label = tk.Label(self.root, text="Speed:")
        self.speed_label.pack(pady=2)
        self.speed_var = tk.StringVar(value="Medium")
        self.speed_dropdown = ttk.Combobox(self.root, textvariable=self.speed_var, state="readonly", width=20)
        self.speed_dropdown["values"] = ["Slow", "Medium", "Fast"]
        self.speed_dropdown.pack(pady=2)

        self.style_label = tk.Label(self.root, text="Style:")
        self.style_label.pack(pady=2)
        self.style_var = tk.StringVar(value="Left-to-Right")
        self.style_dropdown = ttk.Combobox(self.root, textvariable=self.style_var, state="readonly", width=20)
        self.style_dropdown["values"] = ["Left-to-Right", "Bottom-to-Top"]
        self.style_dropdown.pack(pady=2)

        # Send button
        self.send_button = tk.Button(self.root, text="Send Message", command=self.send_message)
        self.send_button.pack(pady=10)

        # Status label for showing message send status
        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.pack(pady=5)

    def set_message_input(self, event):
        """Set the selected message into the input field."""
        selected_message = self.message_dropdown.get()
        self.message_input.delete(0, tk.END)
        self.message_input.insert(0, selected_message)

    def send_message(self):
        """Send the message along with speed and style parameters."""
        message = self.message_input.get() or self.message_dropdown.get()
        if not message:
            self.status_label.config(text="Please enter or select a message!", fg="red")
            return

        # Get scrolling parameters
        speed = self.speed_var.get()
        style = self.style_var.get()

        # Combine message and parameters
        message_to_send = f"{message}|{speed}|{style}___"

        # Send message over serial
        try:
            self.ser.write(message_to_send.encode())
            self.status_label.config(text=f"Message Sent: {message_to_send}", fg="green")
        except serial.SerialException as e:
            self.status_label.config(text=f"Error: {e}", fg="red")

    def on_closing(self):
        """Handle the closing event."""
        print("Closing application...")
        self.ser.close()  # Close serial port
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectionApp(root)  # Start with the connection screen
    root.mainloop()
