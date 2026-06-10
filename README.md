# CLAUDIA - AI Gaming Concierge

CLAUDIA is an intelligent gaming companion and recommendation agent built for the **Google Cloud Rapid Agent Hackathon**. She helps gamers discover titles based on complex natural language "vibes" by leveraging semantic vector pipelines and gaming databases.

## 🚀 Hackathon Tech Stack & Architecture

This project strictly utilizes the required Google Cloud and Partner ecosystems with zero competing services:

1. **Core AI Engine**: Google GenAI (`gemini-2.5-flash`) via the Google Cloud platform.
2. **Framework**: Google Agent Development Kit (ADK) to structure the multi-tool routing and runtime environment.
3. **Partner Integration (MongoDB Track)**: Connects directly to a MongoDB Atlas cluster utilizing a `$vectorSearch` index powered by Voyage AI embeddings to execute natural language vibe-matching queries on game metadata documents.
4. **Ecosystem Extension**: Utilizes a Steam Model Context Protocol (MCP) server via Stdio to inject live community reviews and player metrics seamlessly.

---

## 🛠️ Local Setup & Installation

Ensure you have Python 3.10+ and `uv` installed.

1. **Clone the Repository:**
```bash
   git clone [https://github.com/deep-singh-ctrl/game_scout.git](https://github.com/deep-singh-ctrl/game_scout.git)
   cd game_scout

    Configure Environment Variables:
    Create a .env file in the root directory:

Code snippet

   CONNECTION_STRING="your-mongodb-atlas-connection-string"
   GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
   GOOGLE_CLOUD_LOCATION="your-gcp-region"

    Install Dependencies & Launch Locally:
    Run the ADK development server locally using uv:

Bash

   uv run adk run web

☁️ Cloud Deployment Instructions

To compile and deploy the agent along with its interactive Web UI wrapper directly onto Google Cloud Run, execute the following CLI command:
Bash

uv run adk deploy cloud_run --with_ui . -- \
  --region="your-gcp-region" \
  --set-env-vars="CONNECTION_STRING=your_mongodb_string,GOOGLE_CLOUD_PROJECT=your-gcp-project-id,GOOGLE_CLOUD_LOCATION=your-gcp-region"

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.