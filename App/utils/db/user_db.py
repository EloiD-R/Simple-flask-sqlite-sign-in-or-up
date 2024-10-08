import sqlite3

class userDB:
    def __init__(self, name: str = "user_db"):
        # connect to an existing SQLite database or create a new one
        self.db_name = name
        self.conn = sqlite3.connect(self.db_name + ".db")
        self.cursor = self.conn.cursor()

        # Example: Create a table and the db if not existing
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                creator_ip TEXT NOT NULL
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
        print("\n\t all emails :", end="")
        print(emails)
        print("\n")
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

    def create_user(self, username, email, password, creator_ip):
        self.cursor.execute("INSERT INTO users (username, email, password, creator_ip) VALUES (?, ?, ?, ?)", (username, email, password, creator_ip))
        print(f"created user with email : {email} and username : {username} ")
        self.conn.commit()


    def quit_db(self):
        self.conn.close()


if __name__ == "__main__":
    user_db  = userDB()

    for index in range(0, 5):
        user_db.create_user(f'test{index}', f'<EMAIL>{index}', 'password', "127.0.0.1")

    print(user_db.fetch_all_user_data())
    print(user_db.fetch_all_emails())

    for email in user_db.fetch_all_emails():
        if email[0] == "<EMAIL>8":
            print("email exists")
            break
        else:
            continue