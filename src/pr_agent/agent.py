"""GitHub Pull Request Agent that reviews PRs using various LLM providers."""

import os
from typing import Any, Dict

from dotenv import load_dotenv
from github import Github
from github.GithubException import UnknownObjectException
from openai import OpenAI


class PRAgent:
    """A GitHub Pull Request agent that reviews PRs using various LLM providers."""

    def __init__(self, dry_run: bool = False) -> None:
        """Initialize the PR agent.

        Args:
            dry_run: If True, don't make any actual API calls.
        """
        self.dry_run = dry_run
        self.llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.llm_model = os.getenv("LLM_MODEL", "gpt-4-1106-preview")

        if not dry_run:
            self._init_github()
            self._init_llm()

    def _init_github(self) -> None:
        """Initialize GitHub client."""
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("GITHUB_TOKEN environment variable is required")

        repo_owner = os.getenv("REPO_OWNER")
        repo_name = os.getenv("REPO_NAME")
        if not repo_owner or not repo_name:
            raise ValueError("REPO_OWNER and REPO_NAME environment variables are required")

        self.github = Github(github_token)
        self.repo = self.github.get_repo(f"{repo_owner}/{repo_name}")

    def _init_llm(self) -> None:
        """Initialize LLM client based on provider."""
        if self.llm_provider == "openai":
            openai_key = os.getenv("OPENAI_API_KEY")
            if not openai_key:
                raise ValueError("OPENAI_API_KEY environment variable is required")
            self.llm_client = OpenAI(api_key=openai_key)
        elif self.llm_provider == "deepseek":
            deepseek_key = os.getenv("DEEPSEEK_API_KEY")
            if not deepseek_key:
                raise ValueError("DEEPSEEK_API_KEY environment variable is required")
            # Initialize Deepseek client here
            raise NotImplementedError("Deepseek support not implemented yet")
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")

    def get_pr_changes(self, pr_number: int) -> Dict[str, Any]:
        """Get changes from a PR.

        Args:
            pr_number: The PR number to get changes from.

        Returns:
            A dictionary containing PR changes.
        """
        if self.dry_run:
            return {
                "title": "Example PR Title",
                "body": "Example PR description",
                "files": ["file1.py", "file2.py"],
                "diff": "Example diff content",
            }

        try:
            pr = self.repo.get_pull(pr_number)
        except UnknownObjectException:
            raise ValueError(f"PR #{pr_number} not found")

        changes = {"title": pr.title, "body": pr.body or "", "files": [], "diff": ""}

        try:
            files = pr.get_files()
            changes["files"] = [f.filename for f in files]
            changes["diff"] = files.get_page(0)[0].patch
        except Exception as e:
            raise ValueError(f"Failed to get PR changes: {str(e)}")

        return changes

    def review_pr(self, pr_number: int) -> Dict[str, Any]:
        """Review a PR using the configured LLM provider.

        Args:
            pr_number: The PR number to review.

        Returns:
            A dictionary containing review results.
        """
        changes = self.get_pr_changes(pr_number)
        if self.dry_run:
            return {"summary": "This is a dry run review.", "original_changes": changes}

        # TODO: Implement actual LLM-based review
        raise NotImplementedError("LLM-based review not implemented yet")

    def update_pr_description(self, pr_number: int, review_results: Dict[str, Any]) -> None:
        """Update PR description with review results.

        Args:
            pr_number: The PR number to update.
            review_results: The review results to add to the description.
        """
        if self.dry_run:
            print("Dry run: Would update PR description with:")
            print(review_results["summary"])
            return

        try:
            pr = self.repo.get_pull(pr_number)
            new_body = f"{pr.body or ''}\n\n## AI Review\n{review_results['summary']}"
            pr.edit(body=new_body)
        except Exception as e:
            raise ValueError(f"Failed to update PR description: {str(e)}")


def main() -> None:
    """Run the PR agent from command line."""
    load_dotenv()
    agent = PRAgent()

    # When running in GitHub Actions
    pr_number = int(os.getenv("PR_NUMBER", "0"))
    if pr_number > 0:
        review_results = agent.review_pr(pr_number)
        agent.update_pr_description(pr_number, review_results)
