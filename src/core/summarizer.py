"""Generate summaries from parsed GitHub data."""

from collections import Counter
from typing import Dict, List


class Summarizer:
    """Analyzes repository activity and generates summaries."""

    @staticmethod
    def summarize_commits(commits: List[Dict[str, str]]) -> str:
        """Generate a simple summary of commit activity."""
        if not commits:
            return "No commits found."

        messages = [commit["message"].lower() for commit in commits]

        keywords = []
        for msg in messages:
            if "fix" in msg:
                keywords.append("bug fixes")
            if "add" in msg or "feature" in msg:
                keywords.append("new features")
            if "refactor" in msg:
                keywords.append("refactoring")
            if "remove" in msg:
                keywords.append("removals")

        keyword_counts = Counter(keywords)

        summary_parts = [
            f"{len(commits)} commits were made recently."
        ]

        if keyword_counts:
            dominant = ", ".join(
                f"{k} ({v})" for k, v in keyword_counts.items()
            )
            summary_parts.append(f"Main activity: {dominant}.")

        return " ".join(summary_parts)

    @staticmethod
    def summarize_issues(issues: List[Dict[str, str]]) -> str:
        """Summarize issue activity."""
        if not issues:
            return "No issues found."

        open_issues = sum(1 for issue in issues if issue["state"] == "open")

        return (
            f"{len(issues)} issues found, "
            f"with {open_issues} currently open."
        )

    @staticmethod
    def summarize_pull_requests(pulls: List[Dict[str, str]]) -> str:
        """Summarize pull request activity."""
        if not pulls:
            return "No pull requests found."

        open_pulls = sum(1 for pr in pulls if pr["state"] == "open")

        return (
            f"{len(pulls)} pull requests found, "
            f"with {open_pulls} currently open."
        )