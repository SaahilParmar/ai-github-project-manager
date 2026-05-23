"""Detect risks in repository activity."""

from typing import Dict, List


class RiskDetector:
    """Identifies potential risks in project activity."""

    @staticmethod
    def detect_commit_risks(commits: List[Dict[str, str]]) -> List[str]:
        """Analyze commit patterns for risks."""
        if not commits:
            return ["No commits found: project may be inactive."]

        messages = [commit["message"].lower() for commit in commits]

        risks = []

        fix_count = sum("fix" in msg for msg in messages)
        if fix_count > len(commits) * 0.5:
            risks.append("High number of bug fixes: potential instability.")

        if len(commits) < 3:
            risks.append("Low commit activity: possible slowdown.")

        return risks

    @staticmethod
    def detect_issue_risks(issues: List[Dict[str, str]]) -> List[str]:
        """Analyze issues for risks."""
        if not issues:
            return []

        open_issues = sum(1 for issue in issues if issue["state"] == "open")

        risks = []

        if open_issues > len(issues) * 0.7:
            risks.append("High number of open issues: backlog may be growing.")

        return risks

    @staticmethod
    def detect_pr_risks(pulls: List[Dict[str, str]]) -> List[str]:
        """Analyze pull requests for risks."""
        if not pulls:
            return []

        open_pulls = sum(1 for pr in pulls if pr["state"] == "open")

        risks = []

        if open_pulls > 5:
            risks.append("Too many open pull requests: review bottleneck.")

        return risks

    @staticmethod
    def aggregate_risks(
        commits: List[Dict[str, str]],
        issues: List[Dict[str, str]],
        pulls: List[Dict[str, str]],
    ) -> List[str]:
        """Combine all detected risks."""
        risks = []

        risks.extend(RiskDetector.detect_commit_risks(commits))
        risks.extend(RiskDetector.detect_issue_risks(issues))
        risks.extend(RiskDetector.detect_pr_risks(pulls))

        if not risks:
            return ["No major risks detected."]

        return risks