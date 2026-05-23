"""Configuration module for environment variables."""

import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is not set.")

BASE_URL = "https://api.github.com"
