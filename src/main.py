"""Entry point for AI GitHub Project Manager."""

from src.github.fetcher import GitHubFetcher


def main() -> None:
    """Run the application."""
    repo = input("Enter GitHub repo (owner/repo): ").strip()

    fetcher = GitHubFetcher()

    commits = fetcher.get_commits(repo)
    issues = fetcher.get_issues(repo)
    pulls = fetcher.get_pull_requests(repo)

    print(f"Commits fetched: {len(commits)}")
    print(f"Issues fetched: {len(issues)}")
    print(f"Pull requests fetched: {len(pulls)}")


if __name__ == "__main__":
    main()
