from typing import List, Dict, Any
import github

from gitprovider.base_provider import BaseGitProvider
from logger.logger import get_logger
from settings.config import get_settings

class GithubProvider(BaseGitProvider):
    def __init__(self, pr_url: str):
        super().__init__(pr_url)
        self.github_client = github.Github(get_settings().get("github.token"))
        self._parse_pr_url(pr_url)

    def _parse_pr_url(self, pr_url: str) -> None:
        """Parse PR URL to extract owner, repo, and PR number"""
        try:
            # Expected format: https://github.com/owner/repo/pull/number
            parts = pr_url.split('/')
            self.owner = parts[-4]
            self.repo_name = parts[-3]
            self.pr_number = int(parts[-1])

            # Get repo and PR objects
            self.repo = self.github_client.get_repo(f"{self.owner}/{self.repo_name}")
            self.pr = self.repo.get_pull(self.pr_number)
        except Exception as e:
            get_logger().error(f"Failed to parse PR URL: {e}")
            raise

    def get_files(self) -> List[str]:
        """Get list of files in PR"""
        return [f.filename for f in self.pr.get_files()]

    def get_diff_by_file(self) -> Dict[str, str]:
        """Get diffs for each file in the PR"""
        return {f.filename: f.patch for f in self.pr.get_files()}

    def get_diff(self) -> Dict[str, str]:
        """Get PR diff"""
        diff = {}
        for file in self.pr.get_files():
            diff[file.filename] = file.patch
        return diff

    def get_pr_description(self) -> str:
        """Get PR description"""
        return self.pr.body or ""

    def get_pr_title(self) -> str:
        """Get PR title"""
        return self.pr.title

    def get_pr_branch(self) -> str:
        """Get PR branch name"""
        return self.pr.head.ref

    def get_languages(self) -> Dict[str, Any]:
        """Get repository languages"""
        return self.repo.get_languages()

    def publish_comment(self, comment: str, is_temporary: bool = False) -> None:
        """Publish a comment on the PR"""
        try:
            get_logger().info(f"Publishing comment: {comment}")
            if get_settings().get("config.publish_output", False):
                self.pr.create_issue_comment(comment)
        except Exception as e:
            get_logger().error(f"Failed to publish comment: {e}")
            raise

    def publish_review_comment(self, comment: str, path: str, line_number: int) -> None:
        """Publish a comment on the PR"""
        try:
            get_logger().info(f"Publishing review comment: {comment}")
            if get_settings().get("config.publish_output", False):
                commit = self.repo.get_commit(self.pr.head.sha)
                self.pr.create_review_comment(
                    body = comment,
                    commit = commit,
                    path = path,
                    line=line_number,
                    side="LEFT"
                )
        except Exception as e:
            get_logger().error(f"Failed to publish review comment: {e}")

    def remove_comment(self, comment_id: str) -> None:
        """Remove a comment from the PR"""
        try:
            comment = self.pr.get_issue_comment(int(comment_id))
            comment.delete()
        except Exception as e:
            get_logger().error(f"Failed to remove comment: {e}")
            raise