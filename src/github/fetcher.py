"""GitHub API data fetcher."""

from typing import Any, Dict, List

import requests

from src.config import BASE_URL, GITHUB_TOKEN


class GitHubFetcher:
    """Handles GitHub API requests."""

    def __init__(self) -> None:
        self.headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }

    def _get(self, endpoint: str) -> Any:
        """Perform a GET request to the GitHub API."""
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_commits(self, repo: str) -> List[Dict[str, Any]]:
        """Fetch recent commits."""
        return self._get(f"/repos/{repo}/commits")

    def get_issues(self, repo: str) -> List[Dict[str, Any]]:
        """Fetch issues (excluding pull requests)."""
        data = self._get(f"/repos/{repo}/issues")
        return [item for item in data if "pull_request" not in item]

    def get_pull_requests(self, repo: str) -> List[Dict[str, Any]]:
        """Fetch pull requests."""
        return self._get(f"/repos/{repo}/pulls")
