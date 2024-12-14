import tkinter as tk
import serial
import threading
import time
from collections import deque

class ReceiverApp:
    def __init__(self, root,port,baud_rate):
        self.root = root
        self.root.title("Receiver")
        self.port = port
        self.baud_rate = baud_rate
        # Create a canvas with a scrollable frame
        self.canvas = tk.Canvas(self.root, width=500, height=300)
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=20)

        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.message_frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.message_frame, anchor="nw")

        #scrolling
        self.message_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.message_queue = deque()

        # listen to the serial port
        self.serial_thread = threading.Thread(target=self.listen_for_messages,args=[port], daemon=True)
        self.serial_thread.start()

        self.update_messages()

    def on_frame_configure(self, event):
        """Adjust the scroll region"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_resize(self, event):
        """Adjust frame width """
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def listen_for_messages(self):
        try:
            with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
                while True:
                    if ser.in_waiting > 0:
                        message = ser.readline().decode('utf-8').strip()
                        if message:
                            self.add_message(message)
        except serial.SerialException as e:
            print(f"Error: {e}")

    def add_message(self, message):
        # Add message with timestamp to queue
        timestamp = time.time()
        self.message_queue.append((message, timestamp))

    def update_messages(self):
        # Update displayed messages and remove expired ones
        now = time.time()
        self.message_queue = deque([(msg, ts) for msg, ts in self.message_queue if now - ts < 1800])
        for widget in self.message_frame.winfo_children():
            widget.destroy()

        for message, _ in self.message_queue:
            label = tk.Label(self.message_frame, text=message, font=('Arial', 14), anchor="w", width=50)
            label.pack(anchor="w", padx=5, pady=2)

        self.root.after(1000, self.update_messages) 

if __name__ == "__main__":
    port = input("Enter receiver port")
    root = tk.Tk()
    app = ReceiverApp(root,port,9600)
    root.mainloop()
