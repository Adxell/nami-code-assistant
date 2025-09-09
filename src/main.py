from multiprocessing import context
from fastmcp import FastMCP, Context

from contextlib import contextmanager

from typing import AsyncIterator

from db_manager.db import DatabaseManager as PostgresManager

from settings.setting import settings

from dataclasses import dataclass


@dataclass
class AppContext:
    db: PostgresManager

@contextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage database lifecycle with type-safe context."""
    # Initialize database connection on startup
    db_host = settings.DB_HOST
    db_port = settings.DB_PORT
    db_name = settings.DB_NAME
    db_user = settings.DB_USER
    db_password = settings.DB_PASSWORD

    db = PostgresManager(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    
    try:
        await db.connect()
        print("Database connected.")
        yield AppContext(db=db)
    finally:
        await db.disconnect()

mcp = FastMCP("My Code Assistant", lifespan=app_lifespan)


@mcp.tool
async def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"

@mcp.tool
async def read_file(file_path: str) -> str:
    """Read the contents of a file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return str(e)

@mcp.tool
async def list_directory(directory_path: str) -> str:
    """List the contents of a directory."""
    import os
    return "\n".join(os.listdir(directory_path))

@mcp.tool
async def create_table(ctx: Context, table_name: str, columns: str) -> str:
    """Create a table in the database."""
    db = ctx.request_context.lifespan_context.db
    query = f"CREATE TABLE {table_name} ({columns});"
    try:
        await db.execute_query(query)
        return f"Table {table_name} created successfully."
    except Exception as e:
        return str(e)
    

if __name__ == "__main__":
    mcp.run()