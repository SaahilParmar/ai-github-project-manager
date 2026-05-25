"""CLI entry point."""

import sys

from dotenv import load_dotenv

load_dotenv()

from src.ai.analyzer import AIAnalyzer
from src.core.health_score import HealthScore
from src.core.risk_detector import RiskDetector
from src.core.summarizer import Summarizer
from src.core.task_suggester import TaskSuggester
from src.github.fetcher import GitHubFetcher
from src.github.parser import GitHubParser


def analyze_repo(repo: str) -> None:
    fetcher = GitHubFetcher()

    raw_commits = fetcher.get_commits(repo)
    raw_issues = fetcher.get_issues(repo)
    raw_pulls = fetcher.get_pull_requests(repo)

    commits = GitHubParser.parse_commits(raw_commits)
    issues = GitHubParser.parse_issues(raw_issues)
    pulls = GitHubParser.parse_pull_requests(raw_pulls)

    print("\n--- Summary ---\n")

    print("Commits:")
    print(Summarizer.summarize_commits(commits))

    print("\nIssues:")
    print(Summarizer.summarize_issues(issues))

    print("\nPull Requests:")
    print(Summarizer.summarize_pull_requests(pulls))

    # 🔥 Health Score
    score, insights = HealthScore.calculate(commits, issues, pulls)

    print("\n--- Project Health ---\n")
    print(f"Score: {score} / 10\n")

    for insight in insights:
        print(f"- {insight}")

    # 🔥 Risks
    print("\n--- Risks ---")
    for risk in RiskDetector.aggregate_risks(commits, issues, pulls):
        print(f"- {risk}")

    # 🔥 Suggestions
    print("\n--- Suggested Actions ---")
    for suggestion in TaskSuggester.aggregate_suggestions(
        commits, issues, pulls
    ):
        print(f"- {suggestion}")

    # 🔥 AI Layer
    print("\n--- AI Insights ---")

    analyzer = AIAnalyzer()
    ai_output = analyzer.analyze(commits, issues, pulls)

    print(ai_output)


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python -m src.main analyze <owner/repo>")
        sys.exit(1)

    command = sys.argv[1]
    repo = sys.argv[2]

    if command == "analyze":
        analyze_repo(repo)
    else:
        print("Unknown command")
        sys.exit(1)


if __name__ == "__main__":
    main()