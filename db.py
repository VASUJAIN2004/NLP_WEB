import os
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

try:
    from dotenv import load_dotenv
    load_dotenv()  # local development only; on Vercel use Environment Variables
except ImportError:
    pass


class Database:
    """Postgres-backed user store (works on Vercel, unlike a local JSON file)."""

    def __init__(self):
        self._table_ready = False

    def _connect(self):
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        if not self._table_ready:
            with conn, conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        email TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        password_hash TEXT NOT NULL,
                        created_at TIMESTAMPTZ DEFAULT now()
                    )
                    """
                )
            self._table_ready = True
        return conn

    def insert(self, name, email, password):
        email = (email or "").strip().lower()
        conn = self._connect()
        try:
            with conn, conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (email, name, password_hash) "
                    "VALUES (%s, %s, %s) ON CONFLICT (email) DO NOTHING",
                    (email, name, generate_password_hash(password)),
                )
                return 1 if cur.rowcount == 1 else 0
        finally:
            conn.close()

    def search(self, email, password):
        email = (email or "").strip().lower()
        conn = self._connect()
        try:
            with conn, conn.cursor() as cur:
                cur.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
                row = cur.fetchone()
                return 1 if row and check_password_hash(row[0], password) else 0
        finally:
            conn.close()
