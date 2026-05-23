"""AI-based analysis for GitHub repository."""

import os
from typing import Dict, List

import requests

from src.config import OPENAI_URL


class AIAnalyzer:
    """Uses LLM to generate intelligent insights."""

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
            if self.api_key
            else "",
            "Content-Type": "application/json",
        }

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

        if not self.api_key:
            return "AI Analysis skipped: OPENAI_API_KEY not set."

        prompt = self._build_prompt(commits, issues, pulls)

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a senior AI PM."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        }

        try:
            response = requests.post(
                OPENAI_URL,
                headers=self.headers,
                json=payload,
                timeout=20,
            )
            response.raise_for_status()

            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.HTTPError as e:
            return f"AI Analysis failed (HTTP): {str(e)}"

        except requests.exceptions.RequestException as e:
            return f"AI Analysis failed (Network): {str(e)}"

        except (KeyError, IndexError):
            return "AI Analysis failed: Unexpected response format."