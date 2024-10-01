import sqlite3

class userDB:
    def __init__(self, name: str = "user_db"):
        # connect to an existing SQLite database or create a new one
        self.conn = sqlite3.connect(name + ".db")
        self.cursor = self.conn.cursor()

        # Example: Create a table and the db if not existing
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()


    def fetch_all_user_data(self):
        self.cursor.execute("SELECT * FROM users")
        users_data = self.cursor.fetchall()
        return users_data

    def fetch_all_emails(self):
        self.cursor.execute("SELECT email FROM users")
        emails = self.cursor.fetchall()
        return emails

    def get_password_hash_by_email(self, email):
        self.cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def get_id_by_email(self, email):
        self.cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def get_username_by_email(self, email):
        self.cursor.execute("SELECT username FROM users WHERE email = ?", (email,))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def get_username_by_id(self, id):
        self.cursor.execute("SELECT username FROM users WHERE id = ?", (id,))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def create_user(self, name, email, password):
        self.cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)", (name, email, password))
        self.conn.commit()

    def quit_db(self):
        self.conn.close()


if __name__ == "__main__":
    user_db  = userDB()

    for index in range(0, 5):
        user_db.create_user(f'test{index}', f'<EMAIL>{index}', 'password')

    print(user_db.fetch_all_user_data())
    print(user_db.fetch_all_emails())

    for email in user_db.fetch_all_emails():
        if email[0] == "<EMAIL>8":
            print("email exists")
            break
        else:
            continue