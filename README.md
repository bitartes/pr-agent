# PR Agent

A GitHub Pull Request agent that automatically reviews PRs, suggests improvements, and updates PR descriptions using various LLM providers.

## Features

- Automated PR review using multiple LLM providers (OpenAI, Deepseek)
- Code improvement suggestions
- Automatic PR description updates with summaries
- Support for multiple LLM providers
- Works with both public and private repositories
- Organization repository support
- GitHub Actions integration for automatic PR reviews

## Setup

### Local Setup

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up pre-commit hooks:
   ```bash
   pip install pre-commit
   pre-commit install
   pre-commit install --hook-type commit-msg  # For commit message linting
   ```
5. Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
6. Configure your environment variables in `.env`:
   ```bash
   # GitHub Configuration
   GITHUB_TOKEN=your_github_token_here    # Create at https://github.com/settings/tokens
                                         # Need permissions: repo, pull_requests

   # LLM Configuration
   LLM_PROVIDER=openai                   # or 'deepseek'

   # LLM API Keys
   OPENAI_API_KEY=your_openai_key_here
   DEEPSEEK_API_KEY=your_deepseek_key_here

   # LLM Models (optional)
   OPENAI_MODEL=gpt-4                    # or other OpenAI models
   DEEPSEEK_MODEL=deepseek-chat          # or other Deepseek models

   # Repository Configuration
   REPO_OWNER=your_github_username       # or organization name
   REPO_NAME=your_repository_name
   ```

### GitHub Actions Setup

To use PR Agent in your repository via GitHub Actions:

1. Create `.github/workflows/pr_review.yml` in your repository:
   ```yaml
   name: PR Review

   on:
     pull_request:
       types: [opened, synchronize, reopened]

   jobs:
     review:
       runs-on: ubuntu-latest
       steps:
         - uses: bitartes/pr-agent@v1
           with:
             github_token: ${{ secrets.GITHUB_TOKEN }}
             llm_provider: deepseek        # or 'openai'
             deepseek_key: ${{ secrets.DEEPSEEK_API_KEY }}
             # openai_key: ${{ secrets.OPENAI_API_KEY }}  # uncomment if using OpenAI
             # openai_model: gpt-4        # optional: customize model
   ```

2. Add required secrets in your repository:
   - Go to Settings → Secrets and variables → Actions
   - Add your API keys:
     - `DEEPSEEK_API_KEY` if using Deepseek
     - `OPENAI_API_KEY` if using OpenAI
   - `GITHUB_TOKEN` is automatically provided by GitHub

The workflow will automatically review any new or updated PRs.

## Development

### Code Quality Tools

The project uses several code quality tools:

- **Black**: Code formatting
- **isort**: Import sorting
- **Flake8**: Style guide enforcement
- **MyPy**: Static type checking
- **pre-commit**: Automated code quality checks
- **pytest**: Testing framework

These tools run automatically on each commit via pre-commit hooks.

### Running Tests

```bash
pytest
```

This will run all tests and generate a coverage report.

### Pre-commit Hooks

The following checks run automatically before each commit:
- Code formatting (Black)
- Import sorting (isort)
- Style checks (Flake8)
- Type checking (MyPy)
- Basic file checks (trailing whitespace, YAML validity, etc.)
- Commit message linting (conventional commits)

If any check fails, the commit will be blocked. Fix the issues and try committing again.

## Local Usage

```python
from pr_agent import PRAgent

# Initialize agent
agent = PRAgent()

# Review a specific PR
review_results = agent.review_pr(pr_number=123)

# Update PR description with review
agent.update_pr_description(pr_number=123, review_results=review_results)
```

Or use the test script to list and review PRs interactively:
```bash
python test_pr_agent.py
```

## Configuration

The agent supports two LLM providers:
- OpenAI (GPT-4, GPT-3.5-turbo)
- Deepseek (deepseek-chat)

Switch between providers by setting `LLM_PROVIDER` in your `.env` file or in the GitHub Actions workflow.

## Contributing

1. Fork the repository
2. Set up the development environment as described above
3. Make your changes
4. Ensure all tests pass and code quality checks succeed
5. Submit a pull request

Feel free to submit issues and enhancement requests!
