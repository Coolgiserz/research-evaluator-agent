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
llm:
  basic:
    model: "doubao-1-5-pro-32k-250115"
    api_key: xxxx
    base_url: xxx
  reason:
    model: "doubao-1-5-pro-32k-250115"
    api_key: xxxx
    base_url: xxx
metrics:
  breadth:
    template: prompts/breadth.tpl
    weight: 0.20
  depth:
    template: prompts/depth.tpl
    weight: 0.20
  relevance:
    template: prompts/relevance.tpl
    weight: 0.25
  novelty:
    template: prompts/novelty.tpl
    weight: 0.10
  factuality:
    template: prompts/factuality.tpl
    weight: 0.25
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
  "metric_scores": [
    {
      "metric_name": "breadth",
      "score": 1,
      "comment": "文章仅提到'智能体'，与用户意图'乾坤大挪移'完全无关，未覆盖任何相关武功、招式或原理的内容。"
    },
    {
      "metric_name": "depth",
      "score": 1,
      "comment": "文章仅提到'智能体'，与'乾坤大挪移'的武功、招式和原理完全无关，缺乏任何相关描述或解释。"
    },
    {
      "metric_name": "factuality",
      "score": 1,
      "comment": "文章内容与'乾坤大挪移'无关，未提及任何相关武功、招式或原理，属于严重偏离主题的错误。"
    },
    {
      "metric_name": "novelty",
      "score": 1,
      "comment": "文章内容与用户意图和共享上下文无关，未涉及武功、招式或原理，仅提到'智能体'，缺乏相关性与新颖性。"
    },
    {
      "metric_name": "relevance",
      "score": 1,
      "comment": "文章内容与'乾坤大挪移'这一武功招式完全无关，未涉及任何相关主题。"
    }
  ],
  "overall_score": 1,
  "overall_comment": "该研究在覆盖面、深度、相关性、新颖性与事实性方面表现均不佳。各方面得分极低，缺乏对研究内容的广泛覆盖和深入探讨，创新性不足且可能存在事实问题。"
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