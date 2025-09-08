import logging

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from typing import Optional, List, Dict

logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self, host: str, port: int, database: str, user: str, password: str) -> None:
        self.host: str = host
        self.port: int = port
        self.database: str = database
        self.user: str = user
        self.password: str = password
        self.pool: Optional[Engine] = None

    def connect(self) -> Engine:
        logger.info("Connecting to the database...")
        try:
            self.pool = create_engine(
                f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}",
                pool_size=10,
                max_overflow=20,
                pool_timeout=30,
                pool_recycle=1800,
            )
            logger.info(f"Database connection pool created successfully.")
            return self.pool
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")

    def disconnect(self):
        logger.info("Disconnecting from the database...")
        if self.pool:
            self.pool.dispose()
            self.pool = None
        logger.info("Disconnected from the database.")

    def execute_query(self, query: str, params: Optional[dict] = None) -> List[Dict]:
        if not self.pool:
            raise Exception("Database connection is not established.")
        with self.pool.connect() as connection:
            result = connection.execute(text(query), params or {})
            return [Dict(row) for row in result.fetchall()]