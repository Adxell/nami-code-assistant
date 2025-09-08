from fastmcp import FastMCP

mcp = FastMCP("My Code Assistant")


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