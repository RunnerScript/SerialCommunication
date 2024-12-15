import sqlite3
import time

class DatabaseHandler:
    def __init__(self, db_name="received_messages.db"):
        self.db_name = db_name
        self.db = sqlite3.connect(self.db_name)
        self.cursor = self.db.cursor()
        self.create_table()

    def create_table(self):
        """Create the table in the database if it doesn't exist."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            timestamp REAL
        )
        """)
        self.db.commit()

    def save_message(self, message):
        """Save the received message to the database."""
        timestamp = time.time()
        self.cursor.execute("INSERT INTO messages (message, timestamp) VALUES (?, ?)", (message, timestamp))
        self.db.commit()

    def load_messages(self):
        """Load all messages from the database."""
        self.cursor.execute("SELECT message, timestamp FROM messages")
        return self.cursor.fetchall()

    def remove_message(self, message, timestamp):
        """Remove the message from the database."""
        self.cursor.execute("DELETE FROM messages WHERE message = ? AND timestamp = ?", (message, timestamp))
        self.db.commit()

    def close(self):
        """Close the database connection."""
        self.db.close()

    def cleanup_expired_messages(self):
        """Remove messages older than 30 minutes from the database."""
        expiration_time = time.time() - 30 * 60  # 30 minutes
        self.cursor.execute("DELETE FROM messages WHERE timestamp < ?", (expiration_time,))
        self.db.commit()
