"""Suggest next actions based on repository state."""

from typing import Dict, List


class TaskSuggester:
    """Generates actionable recommendations."""

    @staticmethod
    def suggest_from_commits(
        commits: List[Dict[str, str]],
    ) -> List[str]:
        """Suggest actions based on commit patterns."""
        if not commits:
            return ["Start development: no commits detected."]

        messages = [commit["message"].lower() for commit in commits]

        suggestions = []

        fix_count = sum("fix" in msg for msg in messages)
        if fix_count > len(commits) * 0.5:
            suggestions.append(
                "Focus on stabilizing features before adding new ones."
            )

        if all("fix" not in msg for msg in messages):
            suggestions.append(
                "Consider adding tests to maintain code quality."
            )

        return suggestions

    @staticmethod
    def suggest_from_issues(
        issues: List[Dict[str, str]],
    ) -> List[str]:
        """Suggest actions based on issue state."""
        if not issues:
            return ["Create issues to track tasks and improvements."]

        open_issues = sum(
            1 for issue in issues if issue["state"] == "open"
        )

        suggestions = []

        if open_issues > len(issues) * 0.7:
            suggestions.append(
                "Prioritize resolving open issues to reduce backlog."
            )

        return suggestions

    @staticmethod
    def suggest_from_pulls(
        pulls: List[Dict[str, str]],
    ) -> List[str]:
        """Suggest actions based on pull requests."""
        if not pulls:
            return ["Introduce pull requests for better code review."]

        open_pulls = sum(
            1 for pr in pulls if pr["state"] == "open"
        )

        suggestions = []

        if open_pulls > 5:
            suggestions.append(
                "Review pending pull requests to avoid merge delays."
            )

        return suggestions

    @staticmethod
    def aggregate_suggestions(
        commits: List[Dict[str, str]],
        issues: List[Dict[str, str]],
        pulls: List[Dict[str, str]],
    ) -> List[str]:
        """Combine all suggestions."""
        suggestions = []

        suggestions.extend(
            TaskSuggester.suggest_from_commits(commits)
        )
        suggestions.extend(
            TaskSuggester.suggest_from_issues(issues)
        )
        suggestions.extend(
            TaskSuggester.suggest_from_pulls(pulls)
        )

        if not suggestions:
            return ["Project is in a healthy state."]

        return suggestions