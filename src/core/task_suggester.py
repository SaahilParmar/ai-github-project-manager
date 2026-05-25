"""Advanced task suggestions using behavioral patterns."""

from typing import Dict, List


class TaskSuggester:
    """Suggest contextual improvements."""

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

        messages = [c["message"].lower() for c in commits]

        # 🔴 PR workflow missing
        if commit_count > 3 and pr_count == 0:
            suggestions.append(
                f"{commit_count} commits detected with no pull requests — introduce PR workflow for code review."
            )

        # 🔴 Issue tracking missing
        if commit_count > 5 and issue_count == 0:
            suggestions.append(
                "Active development detected but no issues — use GitHub Issues for structured planning."
            )

        # 🔴 Bug-heavy repo
        bug_keywords = ["fix", "bug", "error"]
        bug_commits = [
            m for m in messages if any(k in m for k in bug_keywords)
        ]

        if commit_count > 0:
            bug_ratio = len(bug_commits) / commit_count

            if bug_ratio > 0.4:
                suggestions.append(
                    f"{int(bug_ratio * 100)}% of commits are bug-related — prioritize stability over new features."
                )

        # 🔴 Repetitive commits
        if commit_count > 3:
            unique_ratio = len(set(messages)) / len(messages)

            if unique_ratio < 0.5:
                suggestions.append(
                    "Commit messages are repetitive — improve commit clarity and structure."
                )

        return suggestions