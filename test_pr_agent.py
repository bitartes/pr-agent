import os
from pr_agent import PRAgent

def list_open_prs(agent):
    """List all open PRs in the repository"""
    if not agent.dry_run:
        print("\nOpen PRs in repository:")
        print("-" * 50)
        for pr in agent.repo.get_pulls(state='open'):
            print(f"PR #{pr.number}: {pr.title}")
        print("-" * 50)

def main(dry_run=True):
    try:
        # Initialize PR agent
        agent = PRAgent(dry_run=dry_run)
        
        if not dry_run:
            # Show available PRs
            list_open_prs(agent)
            pr_number = int(input("\nEnter PR number to review: "))
        else:
            pr_number = 1  # Dummy number for dry run
        
        # Review the PR
        print(f"\nRunning PR review {'(dry run)' if dry_run else ''}...")
        review_results = agent.review_pr(pr_number)
        
        # Print the review results
        print("\nReview Results:")
        print("-" * 50)
        print(review_results['summary'])
        
        # Update PR description
        print("\nUpdating PR description...")
        agent.update_pr_description(pr_number, review_results)
        
        if dry_run:
            print("\nThis was a dry run. No APIs were called.")
        else:
            print("\nPR review completed and description updated!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Change to False to use real APIs
    main(dry_run=False)
