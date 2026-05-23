"""Entry point for AI GitHub Project Manager."""

from src.ai.analyzer import AIAnalyzer
from src.core.risk_detector import RiskDetector
from src.core.summarizer import Summarizer
from src.core.task_suggester import TaskSuggester
from src.github.fetcher import GitHubFetcher
from src.github.parser import GitHubParser


def main() -> None:
    """Run the application."""
    repo = input("Enter GitHub repo (owner/repo): ").strip()

    fetcher = GitHubFetcher()

    raw_commits = fetcher.get_commits(repo)
    raw_issues = fetcher.get_issues(repo)
    raw_pulls = fetcher.get_pull_requests(repo)

    commits = GitHubParser.parse_commits(raw_commits)
    issues = GitHubParser.parse_issues(raw_issues)
    pulls = GitHubParser.parse_pull_requests(raw_pulls)

    commit_summary = Summarizer.summarize_commits(commits)
    issue_summary = Summarizer.summarize_issues(issues)
    pr_summary = Summarizer.summarize_pull_requests(pulls)

    risks = RiskDetector.aggregate_risks(commits, issues, pulls)
    suggestions = TaskSuggester.aggregate_suggestions(
        commits, issues, pulls
    )

    print("\n--- Rule-Based Summary ---\n")
    print(f"Commits: {commit_summary}")
    print(f"Issues: {issue_summary}")
    print(f"Pull Requests: {pr_summary}")

    print("\n--- Risk Analysis ---")
    for risk in risks:
        print(f"- {risk}")

    print("\n--- Suggested Actions ---")
    for suggestion in suggestions:
        print(f"- {suggestion}")

    print("\n--- AI Analysis ---\n")

    analyzer = AIAnalyzer()
    ai_output = analyzer.analyze(commits, issues, pulls)

    print(ai_output)


if __name__ == "__main__":
    main()