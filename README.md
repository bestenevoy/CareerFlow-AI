# Deep Research Tutorial

python -m http.server 12800 --directory static
uv run adk web


A comprehensive AI-powered chemistry research system that combines database querying, literature analysis, and automated report generation. This project demonstrates how to build a multi-agent system for scientific research using Google's Agent Development Kit (ADK).

## 🚀 Features

### Core Capabilities
- **Multi-Agent Architecture**: Hierarchical agent system with specialized sub-agents
- **Database Integration**: SQLite-based local database with CSV data loading
- **Literature Analysis**: Automated paper reading and content extraction
- **Report Generation**: AI-powered scientific report creation
- **RESTful API**: Flask-based API for database operations

### Agent System
- **Chemistry Research Agent**: Main orchestrator agent that coordinates research tasks
- **Database Agent**: Handles structured data queries and fact retrieval
- **Deep Research Agent**: Performs literature reviews and generates reports
- **Paper Agent**: Processes individual research papers
- **Report Agent**: Synthesizes findings into comprehensive reports

## 📁 Project Structure

```
deep_research_tutorial/
├── agent/                          # Multi-agent system
│   ├── agent.py                    # Main chemistry research agent
│   ├── callbacks.py                # Agent callback functions
│   ├── llm_config.py              # LLM configuration
│   ├── database_agent/            # Database query agent
│   ├── deep_research_agent/       # Literature research agent
│   │   ├── agent.py               # Deep research orchestrator
│   │   ├── paper_agent/           # Individual paper processor
│   │   └── report_agent/          # Report generation agent
│   └── tools/                     # Agent tools and utilities
├── database_server/               # Database and API services
│   ├── service.py                 # Flask API and database service
│   ├── polymer.csv               # Polymer data
│   ├── paper_metadata.csv        # Paper metadata
│   └── paper_text.csv            # Paper content data
├── my_data.db                    # SQLite database file
├── pyproject.toml                # Project dependencies
└── README.md                     # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.12 or higher
- UV package manager (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd deep_research_tutorial
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   # Create a .env file with your API keys
   echo "OPENAI_API_KEY=your_openai_key_here" > .env
   echo "GOOGLE_API_KEY=your_google_key_here" > .env
   echo "DEEPSEEK_API_KEY=your_deepseek_key_here" > .env
   ```

## 🚀 Quick Start

### 1. Start the Database Server

```bash
python database_server/service.py
```

This will:
- Load CSV data into SQLite database
- Start Flask API server on `http://localhost:5000`
- Make database accessible via REST API

### 2. Use the Agent System in Google ADK Web UI

```bash
uv run adk web
```

## 🤖 Agent Workflow

### 1. User Query Processing
The main chemistry research agent:
- Analyzes user intent
- Creates a step-by-step research plan
- Proposes actions one at a time

### 2. Database Querying
The database agent:
- Searches structured data for facts
- Retrieves relevant paper metadata
- Returns formatted results

### 3. Literature Research
The deep research agent:
- Processes relevant papers in parallel
- Extracts key information
- Synthesizes findings

### 4. Report Generation
The report agent:
- Compiles all findings
- Generates comprehensive reports
- Formats output for user consumption

## 🔍 Example Use Cases

### Chemical Property Queries
```
"What is the melting point of paracetamol?"
"Find solvents for recrystallizing benzoic acid"
"What are the properties of polyimide polymers?"
```

### Literature Research
```
"Recent advancements in asymmetric catalysis for ibuprofen synthesis"
"Biocompatibility studies of PLA polymers"
"Novel methods for polymer characterization"
```

## 🛠️ Configuration

### LLM Configuration
Edit `agent/llm_config.py` to customize:
- Model selection (GPT-4, Claude, etc.)
- API endpoints
- Temperature and other parameters

### Database Configuration
Modify `database_server/service.py` to:
- Change database file path
- Add new data sources
- Customize API endpoints

## 📝 Dependencies

Key dependencies include:
- `google-adk>=1.5.0` - Google Agent Development Kit
- `litellm>=1.73.1` - LLM abstraction layer
- `openai>=1.91.0` - OpenAI API client
- `pandas>=2.3.0` - Data manipulation
- `flask>=3.1.1` - Web framework
- `pydantic>=2.11.7` - Data validation
- `requests>=2.32.4` - HTTP client

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Agent Development Kit (ADK) team
- OpenAI for LLM APIs
- The chemistry research community at DP Technology

## 📞 Support

For questions and support:
- Open an issue on GitHub
- Check the documentation
- Review the example usage

---

**Note**: This is a tutorial project demonstrating AI-powered research workflows. For production use, ensure proper security, validation, and error handling.
