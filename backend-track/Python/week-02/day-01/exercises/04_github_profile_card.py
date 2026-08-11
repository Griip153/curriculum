# Exercise 4 - GitHub profile card
#
# Fetch a public GitHub user's profile from the GitHub API and print their
# name, bio, and follower count in a small formatted "card".
#
# API docs: https://docs.github.com/en/rest/users/users
# Example URL:
#   https://api.github.com/users/torvalds
#
# Expected output shape:
#   Linus Torvalds
#   Followers: 210000
#
# Run: python3 exercises/04_github_profile_card.py

import asyncio
import httpx

USERNAME = "torvalds"

async def github_profile_card():
    # TODO: your code here - follow the same try/except shape as 01_get_rate.py
    pass

asyncio.run(github_profile_card())
