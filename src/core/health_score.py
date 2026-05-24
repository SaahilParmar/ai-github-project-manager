"""Project health scoring system."""

from typing import Dict, List, Tuple


class HealthScore:
    """Calculate project health score with weighted metrics."""

    @staticmethod
    def calculate(
        commits: List[Dict[str, str]],
        issues: List[Dict[str, str]],
        pulls: List[Dict[str, str]],
    ) -> Tuple[float, List[str]]:
        """Return score and tagged insights."""

        score = 10.0
        insights: List[str] = []

        commit_count = len(commits)
        issue_count = len(issues)
        pr_count = len(pulls)

        # 🔴 No PR workflow
        if commit_count > 0 and pr_count == 0:
            score -= 2.5
            insights.append("[HIGH] No pull request workflow detected")

        # 🔴 Low activity
        if commit_count < 3:
            score -= 2.0
            insights.append("[HIGH] Very low development activity")

        # 🟠 Issue imbalance
        if issue_count > commit_count:
            score -= 1.5
            insights.append("[MEDIUM] Issue backlog growing faster than commits")

        # 🟠 Bug-heavy commits
        bug_keywords = ["fix", "bug", "error"]
        bug_commits = [
            c for c in commits
            if any(k in c["message"].lower() for k in bug_keywords)
        ]

        if commit_count > 0 and len(bug_commits) > commit_count * 0.4:
            score -= 1.5
            insights.append("[MEDIUM] High bug-fix frequency")

        # 🟡 No issue tracking
        if issue_count == 0 and commit_count > 5:
            score -= 1.0
            insights.append("[LOW] No issue tracking despite active development")

        # 🟡 No collaboration
        if pr_count < 2 and commit_count > 5:
            score -= 1.0
            insights.append("[LOW] Limited collaboration via pull requests")

        # Clamp score
        score = max(0.0, round(score, 1))

        return score, insights