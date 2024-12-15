# Project Demo: Transmitter and Receiver Application

## Overview
This project demonstrates a serial communication system with two key components:

1. **Transmitter Application**: A GUI-based application built using `Tkinter` that allows users to send messages via a specified serial port.
2. **Receiver Application**: An application that listens to the specified serial port and processes the incoming messages.

The transmitter application supports database integration to manage messages, a dropdown menu for quick selection of predefined messages, and serial communication with error handling.

---

## Features
- **Transmitter Application**:
  - GUI-based with port connection setup.
  - Allows sending messages via serial communication.
  - Supports loading predefined messages from a database.
  - Error handling for serial communication.

- **Receiver Application**:
  - Receives and processes incoming messages.
  - Displays received messages in a scrollable list.
  - Supports message expiration (older than 10 minutes are removed).
  - Database storage for received messages.

---

## Installation

### Prerequisites
- Python 3.x installed on your system.
- Required Python libraries: `tkinter`, `sqlite3`, and `pyserial`.

### Steps
1. Clone the repository or copy the code files to your local machine.
2. Install the required libraries:
   ```bash
   pip install pyserial


3.Run the Receiver application:
   python receiver.py
4.Run the Transmitter application:
   python transmitter.py