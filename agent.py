# --- Import all necessary libraries ---

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from dotenv import load_dotenv
import os

load_dotenv()

# For database access, use a connection string:
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
# For Atlas management, use API credentials:
# ATLAS_CLIENT_ID = "YOUR_ATLAS_CLIENT_ID"
# ATLAS_CLIENT_SECRET = "YOUR_ATLAS_CLIENT_SECRET"

root_agent = Agent(
    model="gemini-flash-latest",
    name="claudia",
    instruction="""Help users query and manage MongoDB databases AND fetch Steam game reviews.

Start by asking the user his name and the genre of games he wants as well as his budget and harware specs.
    
You have access to:
1. MongoDB tools - for database operations (querying games, users, etc.)
2. Steam tools - for fetching game reviews, details, and player stats

Use these tools to return a list of games to the user. Then also ask the user whether he wants additional info
for any specific titles. List that you can fetch user reviews, game descriptions etc. 

When a user asks about game reviews, popularity, or player feedback, use the Steam tools.
When they ask about stored data, use MongoDB tools.""",
    tools=[
        # MongoDB MCP
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "mongodb-mcp-server",
                        "--readOnly",  # Remove for write operations
                    ],
                    env={
                        # For database access, use:
                        "MDB_MCP_CONNECTION_STRING": CONNECTION_STRING,
                        # For Atlas management, use:
                        # "MDB_MCP_API_CLIENT_ID": ATLAS_CLIENT_ID,
                        # "MDB_MCP_API_CLIENT_SECRET": ATLAS_CLIENT_SECRET,
                    },
                ),
                timeout=30,
            ),
        ),
        # Steam Reviews MCP
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "@tmhs/steam-mcp"
                    ],
                    env={},  # No API key needed for public reviews!
                ),
                timeout=30,
            ),
        ),
    ],
)