# Research Evaluator Agent

Research Evaluator Agent is an open-source, multi-agent Python framework for automated evaluation of research articles or text using Large Language Models (LLMs).

## Features

- **Multi-Agent Architecture**: Each evaluation metric is implemented as an independent Agent.
- **Customizable Metrics**: Built-in metrics include breadth, depth, relevance, novelty; add your own via prompt templates.
- **Directed Graph Workflow**: Flexible pipeline with interpreter, evaluator, and aggregator nodes.
- **Multiple Interfaces**: Command Line (CLI), Python SDK, and RESTful HTTP API.
- **Configurable**: YAML configuration and environment variables for API keys and parameters.
- **Robust Output**: Built-in JSON repair and normalization utilities.

## Project Structure

```plain
├── README.md              # This file (English)
├── README_zh.md           # Chinese translation
├── conf.yaml.sample       # Sample configuration file
├── env.sample             # Sample environment variables
├── pyproject.toml         # Project metadata and dependencies
├── src/                   # Source code
│   └── research_evaluator_agent
│       ├── agents         # Agent implementations
│       ├── llms           # LLM factory and wrappers
│       ├── prompts        # Prompt templates and variable definitions
│       ├── utils          # Utilities (JSON repair, logging, etc.)
│       └── server         # FastAPI HTTP server
├── tests/                 # Unit tests
├── LICENSE                # MIT License
└── .gitignore
```

## Installation

### From Source

```bash
git clone https://github.com/your-username/research-evaluator-agent.git
cd research-evaluator-agent
python3 -m venv .venv
source .venv/bin/activate
# Install dependencies with uv
uv sync
```

## Configuration

1. Copy the sample configuration:
   ```bash
   cp conf.yaml.sample conf.yaml
   ```
2. Edit `conf.yaml` and set your values:
   ```yaml
   openai_api_key: "YOUR_API_KEY"
   model: "gpt-4"
   metrics:
     - breadth
     - depth
     - relevance
     - novelty
   ```
3. (Optional) Create a `.env` file:
   ```bash
   cp env.sample .env
   export OPENAI_API_KEY=YOUR_API_KEY
   ```

## Usage

### Command Line Interface (CLI)

```bash
# Evaluate an article and save results to result.json
python cli.py evaluate --input path/to/article.txt --output result.json
```

### Python SDK

```python
from research_evaluator_agent import evaluate_article

result = evaluate_article(
    text="Your article content...",
    metrics=["breadth", "depth", "relevance", "novelty"],
)
print(result)
```

### HTTP API

1. Start the server:
   ```bash
   uvicorn src.research_evaluator_agent.server.app:app --reload
   ```
2. Send a POST request:
   ```bash
   curl -X POST http://localhost:8000/evaluate \
     -H "Content-Type: application/json" \
     -d '{"text": "Article content to evaluate."}'
   ```
   **Response**:
   ```json
   {
     "breadth": 4.5,
     "depth": 4.0,
     "relevance": 4.8,
     "novelty": 4.2
   }
   ```

## Testing

Run unit tests with:

```bash
pytest --maxfail=1 --disable-warnings -q
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on issues, pull requests, and code style.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.