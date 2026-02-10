"""MCP Math Server implementation with stdio transport."""
import asyncio
import sys
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio


# Create the server instance
server = Server("math-server")

# Tool implementations
@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available math tools."""
    return [
        Tool(
            name="add",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "x": {"type": "number", "description": "First number"},
                    "y": {"type": "number", "description": "Second number"},
                },
                "required": ["x", "y"],
            },
        ),
        Tool(
            name="subtract", 
            description="Subtract y from x",
            inputSchema={
                "type": "object",
                "properties": {
                    "x": {"type": "number", "description": "First number"},
                    "y": {"type": "number", "description": "Second number"},
                },
                "required": ["x", "y"],
            },
        ),
        Tool(
            name="multiply",
            description="Multiply two numbers together",
            inputSchema={
                "type": "object", 
                "properties": {
                    "x": {"type": "number", "description": "First number"},
                    "y": {"type": "number", "description": "Second number"},
                },
                "required": ["x", "y"],
            },
        ),
        Tool(
            name="divide",
            description="Divide x by y",
            inputSchema={
                "type": "object",
                "properties": {
                    "x": {"type": "number", "description": "First number"},
                    "y": {"type": "number", "description": "Second number"},
                },
                "required": ["x", "y"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    print(f"Tool called: {name} with args: {arguments}", file=sys.stderr)
    
    if name == "add":
        x = arguments.get("x")
        y = arguments.get("y")
        result = x + y
        print(f"Adding {x} + {y} = {result}", file=sys.stderr)
        return [TextContent(type="text", text=str(result))]
    
    elif name == "subtract":
        x = arguments.get("x") 
        y = arguments.get("y")
        result = x - y
        print(f"Subtracting {y} from {x} = {result}", file=sys.stderr)
        return [TextContent(type="text", text=str(result))]
    
    elif name == "multiply":
        x = arguments.get("x")
        y = arguments.get("y") 
        result = x * y
        print(f"Multiplying {x} × {y} = {result}", file=sys.stderr)
        return [TextContent(type="text", text=str(result))]
    
    elif name == "divide":
        x = arguments.get("x")
        y = arguments.get("y")
        if y == 0:
            print("ERROR: Division by zero attempted", file=sys.stderr)
            raise ValueError("Cannot divide by zero.")
        result = x / y
        print(f"Dividing {x} ÷ {y} = {result}", file=sys.stderr)
        return [TextContent(type="text", text=str(result))]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the MCP server with stdio transport."""
    print("🚀 Starting MCP Math Server with stdio transport", file=sys.stderr)
    
    # Run the stdio server
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    print("👋 MCP Math Server starting...", file=sys.stderr) 
    asyncio.run(main())
