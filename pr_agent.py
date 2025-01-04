import os
from github import Github
from dotenv import load_dotenv
from typing import List, Dict
import openai
import anthropic
from decouple import config
import json

class PRAgent:
    def __init__(self):
        load_dotenv()
        self.github = Github(os.getenv("GITHUB_TOKEN"))
        self.repo = self.github.get_repo(f"{os.getenv('REPO_OWNER')}/{os.getenv('REPO_NAME')}")
        
        # Initialize LLM clients
        self.openai_client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
        self.anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def get_pr_changes(self, pr_number: int) -> Dict:
        """Get the changes from a PR"""
        pr = self.repo.get_pull(pr_number)
        files = pr.get_files()
        
        changes = {
            "title": pr.title,
            "body": pr.body,
            "files": [],
            "diff": ""
        }
        
        for file in files:
            changes["files"].append({
                "filename": file.filename,
                "status": file.status,
                "additions": file.additions,
                "deletions": file.deletions,
                "patch": file.patch
            })
            changes["diff"] += f"\nFile: {file.filename}\n{file.patch}\n"
            
        return changes

    def review_pr(self, pr_number: int) -> Dict:
        """Review a PR and provide feedback"""
        changes = self.get_pr_changes(pr_number)
        
        # Example using OpenAI for review
        review_prompt = f"""
        Please review this pull request and provide:
        1. A summary of changes
        2. Potential improvements
        3. Security concerns (if any)
        4. Code style suggestions
        
        Changes:
        {changes['diff']}
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful code reviewer."},
                {"role": "user", "content": review_prompt}
            ]
        )
        
        return {
            "summary": response.choices[0].message.content,
            "original_changes": changes
        }

    def update_pr_description(self, pr_number: int, review_results: Dict):
        """Update the PR description with the review summary"""
        pr = self.repo.get_pull(pr_number)
        
        new_body = f"""
        # PR Summary
        {review_results['summary']}
        
        ---
        Original Description:
        {pr.body}
        """
        
        pr.edit(body=new_body)

def main():
    agent = PRAgent()
    
    # When running in GitHub Actions
    if os.getenv('GITHUB_EVENT_PATH'):
        with open(os.getenv('GITHUB_EVENT_PATH')) as f:
            event = json.loads(f.read())
            pr_number = event['pull_request']['number']
    else:
        # For local testing
        pr_number = 1  # Replace with actual PR number
    
    review_results = agent.review_pr(pr_number)
    agent.update_pr_description(pr_number, review_results)

if __name__ == "__main__":
    main()
