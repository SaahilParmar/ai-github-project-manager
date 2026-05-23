"""Configuration module for environment variables."""

import os

from dotenv import load_dotenv

load_dotenv()


def get_env_variable(name: str) -> str:
    """Fetch required environment variable or raise error."""
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} environment variable is not set.")
    return value


GITHUB_TOKEN = get_env_variable("GITHUB_TOKEN")
OPENAI_API_KEY = get_env_variable("OPENAI_API_KEY")

BASE_URL = "https://api.github.com"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"