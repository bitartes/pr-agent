"""Tests for the PR Agent."""

from typing import Any, Generator
from unittest.mock import MagicMock, patch

import pytest

from pr_agent import PRAgent


@pytest.fixture
def mock_env(monkeypatch: Any) -> None:
    """Set up test environment variables."""
    monkeypatch.setenv("GITHUB_TOKEN", "test-token")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("REPO_OWNER", "test-owner")
    monkeypatch.setenv("REPO_NAME", "test-repo")
    monkeypatch.setenv("LLM_PROVIDER", "openai")


@pytest.fixture
def mock_github() -> Generator[MagicMock, None, None]:
    """Mock GitHub API."""
    with patch("github.Github") as mock:
        yield mock


def test_init_dry_run() -> None:
    """Test initialization in dry run mode."""
    agent = PRAgent(dry_run=True)
    assert agent.dry_run
    assert agent.llm_provider == "openai"


@pytest.mark.usefixtures("mock_env")
def test_init_live(mock_github: MagicMock) -> None:
    """Test initialization in live mode."""
    mock_repo = MagicMock()
    mock_github.return_value.get_repo.return_value = mock_repo

    agent = PRAgent(dry_run=False)

    assert agent.llm_provider == "openai"
    assert not agent.dry_run
    mock_github.assert_called_once_with("test-token")
    mock_github.return_value.get_repo.assert_called_once_with("test-owner/test-repo")
