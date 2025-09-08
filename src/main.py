from fastmcp import FastMCP

from contextlib import contextmanager

from typing import Iterator

from db_manager.db import DatabaseManager as PostgresManager

from settings.setting import settings

from dataclasses import dataclass


@dataclass
class AppContext:
    db: PostgresManager

@contextmanager
def app_lifespan(server: FastMCP) -> Iterator[AppContext]:
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
        db.connect()
        yield AppContext(db=db)
    finally:
        db.disconnect()

mcp = FastMCP("My Code Assistant", lifespan=app_lifespan)


@mcp.tool
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"

@mcp.tool
def read_file(file_path: str) -> str:
    """Read the contents of a file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return str(e)

@mcp.tool
def list_directory(directory_path: str) -> str:
    """List the contents of a directory."""
    import os
    return "\n".join(os.listdir(directory_path))

if __name__ == "__main__":
    mcp.run()