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


root_agent = Agent(
    model="gemini-3.5-flash",
    name="claudia",
    instruction="""You are CLAUDIA, a gaming concierge.

    CRITICAL: To search games by VIBE (e.g., "dystopian cyberpunk", "cozy farming"):
    
    STEP 1: Call the MongoDB MCP's `aggregate` tool. 
    Pass the user's natural language vibe query string directly into the "$vectorSearch" stage using the "queryText" parameter. 
    (Do NOT attempt to convert the text to numbers; the MongoDB Atlas vector_index handles Voyage AI translation seamlessly).
    
    Use this exact JSON payload format for the `aggregate` tool:
    {{
        "collection": "games_all", 
        "pipeline": [{{
            "$vectorSearch": {{
                "index": "vector_index",
                "path": "about_the_game",
                "queryText": "THE_RAW_USER_VIBE_STRING_HERE",
                "numCandidates": 100,
                "limit": 5
            }}
        }}]
    }}
    
    STEP 2: Review the matched document items and extract game metadata.
    
    STEP 3: Present the matching games cleanly to the user showing their names, prices, and genres.
    
    Conversation Flow Requirements:
    - Actively ask the user for their name, budget constraints, hardware specs, and personal game preferences.
    - Leverage the Steam MCP to fetch supplementary game reviews and player counts when displaying choices.
    - Leverage the MongoDB MCP for direct database lookups.
    """,
    tools=[
        # MongoDB Database MCP Toolset
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "mongodb-mcp-server", "--readOnly"],
                    env={"MDB_MCP_CONNECTION_STRING": CONNECTION_STRING},
                ),
                timeout=30,
            ),
        ),
        # Steam Reviews MCP Toolset
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "@tmhs/steam-mcp"]
                ),
                timeout=30,
            ),
        ),
    ],
)