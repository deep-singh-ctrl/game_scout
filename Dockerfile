# Use a lightweight Python base image
FROM python:3.11-slim

# Install curl and Node.js (Required for npx and your MCP toolsets)
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Globally install MCP server packages so they are built into the image.
# This prevents npx from downloading them on every Cloud Run cold start.
RUN npm install -g mongodb-mcp-server @tmhs/steam-mcp

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Cloud Run expects the server to listen on PORT (default 8080)
ENV PORT=8080
# Ensure Python output isn't buffered so errors immediately show in Cloud Logging
ENV PYTHONUNBUFFERED=1
EXPOSE 8080

# Command to run the application. 
# If you launch your ADK interface via a CLI tool instead (like `adk ui`), 
# update this CMD to reflect that command (e.g., CMD ["adk", "ui", "--port", "8080"])
CMD ["python", "app.py"]