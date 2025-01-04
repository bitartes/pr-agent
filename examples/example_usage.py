"""Example usage of PR Agent."""

from pr_agent import PRAgent


def main() -> None:
    """Run example PR review."""
    # Initialize agent
    agent = PRAgent(dry_run=True)

    # Review PR #1 (dry run)
    review_results = agent.review_pr(1)
    print(review_results)


if __name__ == "__main__":
    main()
