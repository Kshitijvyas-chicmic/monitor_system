import requests
from fastapi import HTTPException
from app.core.config import (
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET,
    GITHUB_REDIRECT_URI
)

def verify_github_code(code: str):
    # 1. Exchange code for access token
    token_res = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": GITHUB_REDIRECT_URI,
        }
    )

    token_data = token_res.json()
    access_token = token_data.get("access_token")

    if not access_token:
        raise HTTPException(401, "Invalid GitHub code")

    # 2. Fetch user profile
    user_res = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    # 3. Fetch primary email
    emails_res = requests.get(
        "https://api.github.com/user/emails",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    primary_email = next(
        (e["email"] for e in emails_res if e.get("primary")),
        None
    )

    if not primary_email:
        raise HTTPException(400, "GitHub email not found")

    return {
        "email": primary_email,
        "name": user_res.get("name") or user_res.get("login"),
        "provider_id": str(user_res.get("id"))
    }
