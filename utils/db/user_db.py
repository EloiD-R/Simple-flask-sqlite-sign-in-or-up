import sqlite3

class userDB:
    def __init__(self):
        # Connect to an existing SQLite database or create a new one
        conn, cursor = self.open_close_bdd(0)

        # Example: Create a table and the db if not existing
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                e_mail TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        self.open_close_bdd(1, conn)

    def open_close_bdd(self, *data):
        if data[0] == 0:
            if __name__ is "__main__":
                conn = sqlite3.connect('../../user_db.db')
            else:
                conn = sqlite3.connect('user_db.db')
            cursor = conn.cursor()
            return conn, cursor
        if data[0] == 1:
            data[1].close()
            return True

    def fetch_all_user_data(self):
        conn, cursor = self.open_close_bdd(0)
        cursor.execute("SELECT * FROM users")
        users_data = cursor.fetchall()
        print(users_data)
        self.open_close_bdd(1, conn)
        return users_data

    def fetch_all_emails(self):
        conn, cursor = self.open_close_bdd(0)
        cursor.execute("SELECT e_mail FROM users")
        all_emails = cursor.fetchall()
        print(f"from fetch_all_emails : {all_emails}")
        self.open_close_bdd(1, conn)
        return all_emails

    def create_user(self, name, e_mail, password):
        conn, cursor = self.open_close_bdd(0)
        cursor.execute("INSERT INTO users (name, e_mail, password) VALUES (?, ?, ?)", (name, e_mail, password))
        conn.commit()
        self.open_close_bdd(1, conn)


# ! DANGEROUS ! EXECUTING THIS CODE WILL DELETE ALL DATA FROM THE DB
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

"""
    conn, cursor = user_db.open_close_bdd(0)
    # Delete the tests (and erase all db
    cursor.execute("DELETE FROM users")
    # Reset id counter to 0
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'users'")
    conn.commit()
    user_db.open_close_bdd(1, conn)
"""