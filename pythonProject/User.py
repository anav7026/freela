
import psycopg2
import os

# Get DATABASE_URL from environment or fallback to default if not set
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/mydatabase")

class User:
    def __init__(self, username, password, total):
        self.username = username
        self.password = password
        self.total = total
        self.spendable_income = float(total * 0.80)
        self.tax_savings = float(total * 0.20)

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "total": self.total
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["username"], data["password"], data["total"])

    @staticmethod
    def get_db_connection():
        """Create and return a connection to the PostgreSQL database."""
        conn = psycopg2.connect(DATABASE_URL)
        return conn

    @classmethod
    def create_user(cls, username, password, total):
        """Method to insert a new user into the database."""
        conn = cls.get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password, total) VALUES (%s, %s, %s)",
                (username, password, total)
            )
            conn.commit()  # Save changes to the database
            cur.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            conn.rollback()  # In case of error, rollback the transaction
            cur.close()
            conn.close()
            return False

    @classmethod
    def get_user_by_username(cls, username):
        """Method to retrieve a user from the database by username."""
        conn = cls.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_data = cur.fetchone()
        cur.close()
        conn.close()
        
        if user_data:
            return cls(user_data[1], user_data[2], user_data[3])  # Assuming columns are [id, username, password, total]
        else:
            return None

    def update_user(self):
        """Method to update an existing user in the database."""
        conn = self.get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE users SET password = %s, total = %s WHERE username = %s",
                (self.password, self.total, self.username)
            )
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            conn.rollback()
            cur.close()
            conn.close()
            return False

    @classmethod
    def authenticate(cls, username, password):
        """Authenticate a user by checking username and password."""
        conn = cls.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user_data = cur.fetchone()
        cur.close()
        conn.close()

        if user_data:
            return cls(user_data[1], user_data[2], user_data[3])  # Assuming columns are [id, username, password, total]
        else:
            return None

