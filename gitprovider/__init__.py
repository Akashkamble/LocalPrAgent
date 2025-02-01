from typing import Type

from .base_provider import BaseGitProvider
from .github_provider import GithubProvider
from settings.config import get_settings

def get_git_provider() -> Type[BaseGitProvider]:
    """Returns the appropriate git provider class based on configuration"""
    provider = get_settings().get("config.git_provider", "github")

    if provider == "github":
        return GithubProvider
    # elif provider == "bitbucket":
    #     return BitbucketProvider
    else:
        raise ValueError(f"Unsupported git provider: {provider}")


def get_git_provider_from_url(pr_url: str) -> BaseGitProvider:
    """Get git provider instance based on PR URL"""
    if "github.com" in pr_url:
        return GithubProvider(pr_url)
    # elif "bitbucket.org" in pr_url:
    #     return BitbucketProvider(pr_url)
    else:
        raise ValueError(f"Unsupported git provider URL: {pr_url}")