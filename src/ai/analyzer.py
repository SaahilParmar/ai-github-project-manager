"""AI Analyzer with safe fallback."""

import os
from typing import Dict, List

import requests


class AIAnalyzer:
    """AI-based analysis (optional)."""

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")

    def analyze(
        self,
        commits: List[Dict[str, str]],
        issues: List[Dict[str, str]],
        pulls: List[Dict[str, str]],
    ) -> str:
        """Return AI insights or fallback."""

        if not self.api_key:
            return "AI not configured."

        try:
            return self._call_openai(commits, issues, pulls)
        except Exception as exc:  # noqa: BLE001
            return f"AI unavailable: {str(exc)}"

    def _build_prompt(
        self,
        commits: List[Dict[str, str]],
        issues: List[Dict[str, str]],
        pulls: List[Dict[str, str]],
    ) -> str:
        """Build structured prompt."""

        commit_msgs = [c["message"] for c in commits[:10]]
        issue_titles = [i["title"] for i in issues[:10]]
        pr_titles = [p["title"] for p in pulls[:10]]

        return (
            "You are a senior technical product manager.\n\n"
            "Analyze repository activity and give sharp insights.\n\n"
            "Return:\n"
            "1. Key observation\n"
            "2. Risk\n"
            "3. Action\n\n"
            f"Commits:\n{commit_msgs}\n\n"
            f"Issues:\n{issue_titles}\n\n"
            f"Pull Requests:\n{pr_titles}\n"
        )

    def _call_openai(
        self,
        commits: List[Dict[str, str]],
        issues: List[Dict[str, str]],
        pulls: List[Dict[str, str]],
    ) -> str:
        """Call OpenAI API."""

        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": self._build_prompt(commits, issues, pulls),
                }
            ],
            "temperature": 0.3,
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code != 200:
            return f"AI failed ({response.status_code})"

        data = response.json()

        return data["choices"][0]["message"]["content"]