"""Smarter summarization logic."""

from typing import Dict, List


class Summarizer:
    """Summarize repository activity."""

    @staticmethod
    def summarize_commits(commits: List[Dict[str, str]]) -> str:
        count = len(commits)

        if count == 0:
            return "No commits found."

        return f"{count} commits analyzed. Recent activity level: {'high' if count > 10 else 'moderate' if count > 3 else 'low'}."

    @staticmethod
    def summarize_issues(issues: List[Dict[str, str]]) -> str:
        count = len(issues)

        if count == 0:
            return "No issues reported."

        return f"{count} issues currently open. Indicates {'active feedback' if count > 5 else 'manageable backlog'}."

    @staticmethod
    def summarize_pull_requests(pulls: List[Dict[str, str]]) -> str:
        count = len(pulls)

        if count == 0:
            return "No pull requests found."

        return f"{count} pull requests detected. Suggests {'active collaboration' if count > 3 else 'limited collaboration'}."