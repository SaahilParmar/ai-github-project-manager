"""Advanced risk detection based on repository patterns."""

from typing import Dict, List


class RiskDetector:
    """Detect risks using heuristics."""

    @staticmethod
    def aggregate_risks(
        commits: List[Dict[str, str]],
        issues: List[Dict[str, str]],
        pulls: List[Dict[str, str]],
    ) -> List[str]:
        risks = []

        commit_count = len(commits)
        issue_count = len(issues)
        pr_count = len(pulls)

        # 🔴 No PR usage
        if commit_count > 0 and pr_count == 0:
            risks.append(
                "Commits are being made without pull requests — risk of no code review."
            )

        # 🔴 Too many issues vs commits
        if issue_count > commit_count:
            risks.append(
                "More issues than commits — backlog may be growing without resolution."
            )

        # 🔴 Bug-heavy commits
        bug_keywords = ["fix", "bug", "error", "issue"]
        bug_commits = [
            c for c in commits
            if any(k in c["message"].lower() for k in bug_keywords)
        ]

        if len(bug_commits) > commit_count * 0.4:
            risks.append(
                "High number of bug-related commits — potential stability issues."
            )

        # 🔴 Low activity
        if commit_count < 3:
            risks.append(
                "Low commit activity — project may be inactive or in early stage."
            )

        # 🔴 Issues without PRs
        if issue_count > 0 and pr_count == 0:
            risks.append(
                "Issues exist but no pull requests — possible lack of implementation progress."
            )

        return risks