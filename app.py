import os
from agent import root_agent

if __name__ == "__main__":
    # Cloud Run dynamically provides a PORT environment variable (defaults to 8080)
    port = int(os.environ.get("PORT", 8080))
    host = "0.0.0.0"
    
    print(f"Starting GameScout ADK Web Interface on {host}:{port}...")
    
    # Launch the agent's web interface, securely passing the host and port parameters
    # required by Cloud Run so it can correctly route external web traffic.
    root_agent.ui.launch(server_name=host, server_port=port)