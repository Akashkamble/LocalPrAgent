from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseGitProvider(ABC):
    def __init__(self, pr_url: str):
        self.pr_url = pr_url
        self.pr = None
        self.repo = None

    @abstractmethod
    def get_files(self) -> List[str]:
        """Get list of files in PR"""
        pass

    @abstractmethod
    def get_diff_by_file(self) -> Dict[str, str]:
        """Get diffs for each file in the PR"""
        pass

    @abstractmethod
    def get_diff(self) -> Dict[str, str]:
        """Get PR diff"""
        pass

    @abstractmethod
    def get_pr_description(self) -> str:
        """Get PR description"""
        pass

    @abstractmethod
    def get_pr_title(self) -> str:
        """Get PR title"""
        pass

    @abstractmethod
    def get_pr_branch(self) -> str:
        """Get PR branch name"""
        pass

    @abstractmethod
    def get_languages(self) -> Dict[str, Any]:
        """Get repository languages"""
        pass

    @abstractmethod
    def publish_comment(self, comment: str, is_temporary: bool = False) -> None:
        """Publish a comment on the PR"""
        pass

    @abstractmethod
    def publish_review_comment(self, comment: str, path: str, line_number: int) -> None:
        """Publish a comment on the PR"""
        pass

    @abstractmethod
    def remove_comment(self, comment_id: str) -> None:
        """Remove a comment from the PR"""
        pass

    def get_main_language(self) -> str:
        """Get the main language of the repository"""
        languages = self.get_languages()
        if not languages:
            return "Unknown"
        return max(languages.items(), key=lambda x: x[1])[0]