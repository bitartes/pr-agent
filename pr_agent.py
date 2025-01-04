import os
from github import Github
from github.GithubException import UnknownObjectException
from dotenv import load_dotenv
from typing import List, Dict
from openai import OpenAI
import json

class PRAgent:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        if not dry_run:
            load_dotenv()
            self.github = Github(os.getenv("GITHUB_TOKEN"))
            try:
                self.repo = self.github.get_repo(f"{os.getenv('REPO_OWNER')}/{os.getenv('REPO_NAME')}")
                # Test repo access
                self.repo.full_name
            except Exception as e:
                raise Exception(f"Could not access repository: {str(e)}")
            
            # Initialize LLM client
            self.llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()
            if self.llm_provider == "openai":
                self.llm_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                self.llm_model = os.getenv("OPENAI_MODEL", "gpt-4")
            elif self.llm_provider == "deepseek":
                self.llm_client = OpenAI(
                    api_key=os.getenv("DEEPSEEK_API_KEY"),
                    base_url="https://api.deepseek.com"
                )
                self.llm_model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
            else:
                raise Exception(f"Unsupported LLM provider: {self.llm_provider}")

    def get_pr_changes(self, pr_number: int) -> Dict:
        """Get the changes from a PR"""
        if self.dry_run:
            return {
                "title": "Test PR",
                "body": "Original PR description",
                "files": [],
                "diff": "Mock diff content"
            }

        try:
            pr = self.repo.get_pull(pr_number)
        except UnknownObjectException:
            raise Exception(f"PR #{pr_number} not found. Please make sure:\n"
                          f"1. The PR exists in {self.repo.full_name}\n"
                          f"2. You have the correct permissions to access it\n"
                          f"3. The PR number is correct")
        
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
        if self.dry_run:
            return {
                "summary": """
                Mock Review Results:
                - This is a simulated review
                - No actual API calls were made
                
                Suggestions:
                1. This is a mock suggestion
                2. Another mock suggestion
                """,
                "original_changes": self.get_pr_changes(pr_number)
            }

        try:
            changes = self.get_pr_changes(pr_number)
        except Exception as e:
            raise Exception(f"Failed to retrieve PR changes: {str(e)}")
        
        review_prompt = f"""
        Please review this pull request and provide:
        1. A summary of changes
        2. Potential improvements
        3. Security concerns (if any)
        4. Code style suggestions
        
        Changes:
        {changes['diff']}
        """
        
        try:
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": "You are a helpful code reviewer."},
                    {"role": "user", "content": review_prompt}
                ]
            )
            
            # Both OpenAI and Deepseek use similar response format
            content = response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Failed to generate review using {self.llm_provider}: {str(e)}")
        
        return {
            "summary": content,
            "original_changes": changes
        }

    def update_pr_description(self, pr_number: int, review_results: Dict):
        """Update the PR description with the review summary"""
        if self.dry_run:
            print("Dry run: Would update PR description with:")
            print(review_results['summary'])
            return

        try:
            pr = self.repo.get_pull(pr_number)
        except UnknownObjectException:
            raise Exception(f"PR #{pr_number} not found. Please make sure:\n"
                          f"1. The PR exists in {self.repo.full_name}\n"
                          f"2. You have the correct permissions to access it\n"
                          f"3. The PR number is correct")
        
        new_body = f"""
        # PR Summary (reviewed by {self.llm_provider.title()})
        {review_results['summary']}
        
        ---
        Original Description:
        {pr.body}
        """
        
        try:
            pr.edit(body=new_body)
        except Exception as e:
            raise Exception(f"Failed to update PR description: {str(e)}")

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
    
    try:
        review_results = agent.review_pr(pr_number)
        agent.update_pr_description(pr_number, review_results)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
