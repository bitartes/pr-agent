# PR Agent

A GitHub Pull Request agent that automatically reviews PRs, suggests improvements, and updates PR descriptions using various LLM providers.

## Features

- Automated PR review using multiple LLM providers (OpenAI, Anthropic)
- Code improvement suggestions
- Automatic PR description updates with summaries
- Support for multiple LLM providers

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
4. Configure your environment variables in `.env`:
   - Add your GitHub token
   - Add LLM API keys (OpenAI, Anthropic, etc.)
   - Set your repository details

## Usage

```python
from pr_agent import PRAgent

agent = PRAgent()
review_results = agent.review_pr(pr_number=123)
agent.update_pr_description(pr_number=123, review_results=review_results)
```

## Configuration

The agent uses environment variables for configuration. Required variables:

- `GITHUB_TOKEN`: Your GitHub personal access token
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key
- `REPO_OWNER`: GitHub repository owner
- `REPO_NAME`: GitHub repository name

## Contributing

Feel free to submit issues and enhancement requests!
