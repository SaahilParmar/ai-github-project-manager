"""Parse and structure GitHub data."""

from typing import Any, Dict, List


class GitHubParser:
    """Transforms raw GitHub data into structured signals."""

    @staticmethod
    def parse_commits(
        commits: List[Dict[str, Any]],
    ) -> List[Dict[str, str]]:
        """Extract key commit information."""
        return [
            {
                "message": commit["commit"]["message"],
                "author": commit["commit"]["author"]["name"],
                "date": commit["commit"]["author"]["date"],
            }
            for commit in commits
        ]

    @staticmethod
    def parse_issues(
        issues: List[Dict[str, Any]],
    ) -> List[Dict[str, str]]:
        """Extract key issue information."""
        return [
            {
                "title": issue["title"],
                "state": issue["state"],
                "created_at": issue["created_at"],
            }
            for issue in issues
        ]

    @staticmethod
    def parse_pull_requests(
        pulls: List[Dict[str, Any]],
    ) -> List[Dict[str, str]]:
        """Extract key pull request information."""
        return [
            {
                "title": pr["title"],
                "state": pr["state"],
                "created_at": pr["created_at"],
            }
            for pr in pulls
        ]