"""CLI tool to test PR Agent functionality."""

import argparse

from dotenv import load_dotenv

from pr_agent import PRAgent


def list_open_prs(agent: PRAgent) -> None:
    """List all open PRs in the repository."""
    if not agent.dry_run:
        print("\nOpen PRs in repository:")
        print("-" * 50)
        for pr in agent.repo.get_pulls(state="open"):
            print(f"PR #{pr.number}: {pr.title}")
        print("-" * 50)


def main() -> None:
    """Run the PR agent CLI tool."""
    # Load environment variables first
    load_dotenv()

    parser = argparse.ArgumentParser(description="PR Agent CLI tool")
    parser.add_argument(
        "--live", action="store_true", help="Run in live mode (requires GitHub token)"
    )
    args = parser.parse_args()

    try:
        # Initialize PR agent
        agent = PRAgent(dry_run=not args.live)

        if not agent.dry_run:
            # Show which LLM provider we're using
            print(f"\nUsing {agent.llm_provider.upper()} ({agent.llm_model})")

            # Show available PRs
            list_open_prs(agent)
            pr_number = int(input("\nEnter PR number to review: "))
        else:
            pr_number = 1  # Dummy number for dry run

        # Review the PR
        print(f"\nRunning PR review ({'dry run' if agent.dry_run else ''})...")
        review_results = agent.review_pr(pr_number)

        # Print the review results
        print("\nReview Results:")
        print("-" * 50)
        print(review_results["summary"])

        # Update PR description
        print("\nUpdating PR description...")
        agent.update_pr_description(pr_number, review_results)

        if agent.dry_run:
            print("\nThis was a dry run. No APIs were called.")
        else:
            print("\nPR review completed successfully!")

    except Exception as e:
        print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()
