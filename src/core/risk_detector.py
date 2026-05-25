"""Advanced risk detection."""

from typing import Dict, List


class RiskDetector:
    """Detect deeper risks."""

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

        messages = [c["message"].lower() for c in commits]

        # 🔴 No PRs
        if commit_count > 0 and pr_count == 0:
            risks.append(
                "No pull requests detected — high risk of unreviewed code."
            )

        # 🔴 Bug-heavy
        bug_keywords = ["fix", "bug", "error"]
        bug_commits = [
            m for m in messages if any(k in m for k in bug_keywords)
        ]

        if commit_count > 0 and len(bug_commits) > commit_count * 0.4:
            risks.append(
                "High proportion of bug-fix commits — indicates unstable system."
            )

        # 🔴 No issues
        if commit_count > 5 and issue_count == 0:
            risks.append(
                "No issue tracking despite active commits — lack of structured workflow."
            )

        # 🔴 Low activity
        if commit_count < 3:
            risks.append(
                "Very low commit activity — project may be inactive."
            )

        return risks