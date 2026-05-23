"""AI-based analysis for GitHub repository."""

import os
from typing import Dict, List

import requests


class AIAnalyzer:
    """Uses LLM to generate intelligent insights."""

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set.")

        self.url = "https://api.openai.com/v1/chat/completions"

    def _build_prompt(
        self,
        commits: List[Dict[str, str]],
        issues: List[Dict[str, str]],
        pulls: List[Dict[str, str]],
    ) -> str:
        """Create structured prompt for AI."""
        commit_messages = [c["message"] for c in commits[:10]]
        issue_titles = [i["title"] for i in issues[:10]]
        pr_titles = [p["title"] for p in pulls[:10]]

        return (
            "You are a senior technical product manager.\n\n"
            "Analyze the repository activity and respond STRICTLY in "
            "this format:\n\n"
            "### Summary\n"
            "- ...\n\n"
            "### Key Risks\n"
            "- ...\n\n"
            "### Recommended Actions\n"
            "- ...\n\n"
            "Be concise, specific, and actionable.\n\n"
            f"Commits:\n{commit_messages}\n\n"
            f"Issues:\n{issue_titles}\n\n"
            f"Pull Requests:\n{pr_titles}\n"
        )

    def analyze(
        self,
        commits: List[Dict[str, str]],
        issues: List[Dict[str, str]],
        pulls: List[Dict[str, str]],
    ) -> str:
        """Send data to AI and get analysis."""
        prompt = self._build_prompt(commits, issues, pulls)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a senior AI PM."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        }

        response = requests.post(
            self.url, headers=headers, json=payload, timeout=20
        )
        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]