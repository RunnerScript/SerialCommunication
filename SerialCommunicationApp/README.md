# Project Demo: Transmitter and Receiver Application

## Overview
This project demonstrates a serial communication system with two key components:
1. **Transmitter Application**: A GUI-based application built using `Tkinter` that allows users to send messages via a specified serial port.
2. **Receiver Application**: An application  that listens to the specified serial port and processes the incoming messages.

The transmitter application supports database integration to manage messages, a dropdown menu for quick selection of predefined messages, and serial communication with error handling.

---

## Features

## Installation

### Prerequisites
- Python 3.x installed on your system.
- Required Python libraries: `tkinter`, `sqlite3`, and `pyserial`.

### Steps
1. Clone the repository or copy the code files to your local machine.
2. Install the required libraries:
   ```bash
   pip install pyserial
   ```

3. Run the **Receiver** application:
   ```bash
   python receiver.py
   ```

4. Run the **Transmitter** application:
   ```bash
   python transmitter.py
   ```

---

## Usage

### Transmitter Application
1. **Start the App**:
   - Enter the port to which the transmitter will connect.
   - The GUI interface will launch after the port is specified.

2. **Send a Message**:
   - Enter a message in the input field or select a message from the dropdown.
   - Click **Send Message** to transmit the message over the serial port.
   - The status label will update to indicate if the message was sent successfully or if an error occurred.

3. **Load a Message from the Database**:
   - Select a message from the dropdown menu.
   - Click **Load Message from DB** to populate the input field with the selected message.

4. **Close the App**:
   - Close the app window. The database connection will close automatically.

---

## Example

1. **Input Port**: On startup, input the port (e.g., `COM2`).
2. **Send a Message**:
   - Input `Hello, Receiver!` in the input field and click **Send Message**.
   - The message will be transmitted via the serial port at a baud rate of 9600.

---

## Code Explanation

### Transmitter Application (`transmitter.py`)
- **Database Setup**:
  - Creates a SQLite database (`messages.db`) with a `messages` table if it doesn't exist.
  - Inserts sample messages into the database during initialization.

- **GUI Widgets**:
  - **Entry Field**: For inputting custom messages.
  - **Dropdown Menu**: Populates with messages from the database.
  - **Send Button**: Sends the message over the serial port.
  - **Load Button**: Loads a selected message from the database.

- **Serial Communication**:
  - Sends the message using `pyserial` to the specified port at a baud rate of 9600.

---

## Future Enhancements

1. **Receiver Application**:
   - Develop a receiver app that listens on the specified port and displays incoming messages.
2. **Advanced Features**:
   - Add encryption for messages.
   - Support multiple baud rates and dynamic port selection.
   - Implement a logging mechanism for sent and received messages.

---

## Requirements

Here’s the `requirements.txt` for the project:

```
pyserial
```

To generate the file manually:
```bash
pip freeze > requirements.txt
```

---

## License
This project is released under the MIT License.

---

## Author
- **[Your Name]**

