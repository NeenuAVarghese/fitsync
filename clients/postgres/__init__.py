from typing import Any
from dataclasses import dataclass
from datetime import datetime
from psycopg2.pool import ThreadedConnectionPool


@dataclass
class User:
    username: str
    password: str
    last_sync: datetime
    fitbit_refresh_token: str
    strava_refresh_token: str


class ConnectionClient:
    def __init__(self, connection: Any):
        self.connection = connection

    def get_user_with_password(self, username: str) -> tuple[str, str]:
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT username, password FROM users WHERE username = %s", (username,)
            )
            return cursor.fetchone()


class Client:
    def __init__(self, dsn):
        """
        dsn: postgresql://user:password@host:port/dbname
        """
        self.pool = ThreadedConnectionPool(1, 20, dsn=dsn)
        with self.pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        last_sync TIMESTAMPTZ,
                        fitbit_refresh_token TEXT,
                        strava_refresh_token TEXT
                    );
                    """
                )
                conn.commit()
        self.pool.putconn(conn)

    def __call__(self) -> ConnectionClient:
        cc = ConnectionClient(self.pool.getconn())
        try:
            yield cc
        finally:
            self.pool.putconn(cc.connection)
