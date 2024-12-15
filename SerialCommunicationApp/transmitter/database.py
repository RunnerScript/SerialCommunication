import sqlite3

class DatabaseHandler:
    def __init__(self, db_name="messages.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_message(self, content):
        self.cursor.execute("INSERT INTO messages (content) VALUES (?)", (content,))
        self.conn.commit()

    def get_messages(self):
        self.cursor.execute("SELECT * FROM messages")
        return self.cursor.fetchall()

    def delete_message(self, message_id):
        self.cursor.execute("DELETE FROM messages WHERE id = ?", (message_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db = DatabaseHandler()
    db.add_message("Hello, World!")
    db.add_message("Test Message 1")
    db.add_message("Test Message 2")
    db.close()