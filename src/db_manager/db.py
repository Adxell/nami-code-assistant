import logging

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from typing import Optional, List, Dict

import asyncpg

logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self, host: str, port: int, database: str, user: str, password: str) -> None:
        self.host: str = host
        self.port: int = port
        self.database: str = database
        self.user: str = user
        self.password: str = password
        self.pool: Optional[Engine] = None

    async def connect(self) -> Engine:
        logger.info("Connecting to the database...")
        try:
            self.pool = await asyncpg.create_pool(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                min_size=1,
                max_size=10,
                timeout=30
            )
            logger.info(f"Database connection pool created successfully.")
            return self.pool
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")

    async def disconnect(self):
        logger.info("Disconnecting from the database...")
        if self.pool:
            await self.pool.close()
            logger.info("PostgreSQL connection pool closed")
    
    
    async def disconnect(self):
        logger.info("Disconnecting from the database...")
        if self.pool:
            self.pool.dispose()
            self.pool = None
        logger.info("Disconnected from the database.")

    async def execute_query(self, query: str, params: Optional[dict] = None) -> List[Dict]:
        if not self.pool:
            raise Exception("Database connection is not established.")
        async with self.pool.connect() as connection:
            result = await connection.execute(text(query), params or {})
            return [Dict(row) for row in result.fetchall()]