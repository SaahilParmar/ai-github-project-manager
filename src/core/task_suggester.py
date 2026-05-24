"""Context-aware task suggestions."""

from typing import Dict, List


class TaskSuggester:
    """Suggest actionable improvements."""

    @staticmethod
    def aggregate_suggestions(
        commits: List[Dict[str, str]],
        issues: List[Dict[str, str]],
        pulls: List[Dict[str, str]],
    ) -> List[str]:
        suggestions = []

        commit_count = len(commits)
        issue_count = len(issues)
        pr_count = len(pulls)

        # ✅ Introduce PR workflow
        if commit_count > 0 and pr_count == 0:
            suggestions.append(
                "Introduce pull request workflow to ensure code review and collaboration."
            )

        # ✅ Handle backlog
        if issue_count > commit_count:
            suggestions.append(
                "Prioritize resolving existing issues before adding new features."
            )

        # ✅ Improve stability
        bug_keywords = ["fix", "bug", "error"]
        bug_commits = [
            c for c in commits
            if any(k in c["message"].lower() for k in bug_keywords)
        ]

        if len(bug_commits) > commit_count * 0.4:
            suggestions.append(
                "Focus on stabilizing core functionality before expanding features."
            )

        # ✅ Boost activity
        if commit_count < 3:
            suggestions.append(
                "Increase development activity to maintain project momentum."
            )

        # ✅ Track work properly
        if issue_count == 0:
            suggestions.append(
                "Start using GitHub Issues to track tasks and improvements."
            )

        return suggestions