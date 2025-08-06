# ✅ TikTok OAuth Flask App

from flask import Flask, redirect, request, jsonify
import requests
import os

app = Flask(__name__)

# TikTok credentials from Developer Console
CLIENT_KEY = "sbaw9w8f6124vl12yb"  # replace with your actual
CLIENT_SECRET = "RSidfgGUudLNdkD0R9iqGlZvdniC3x9y"  # replace with yours
REDIRECT_URI = "https://your-app-name.onrender.com/callback"  # set this after deploying

SCOPES = "user.info.basic video.publish"

@app.route("/")
def home():
    return '<a href="/login">Login with TikTok</a>'

@app.route("/login")
def login():
    oauth_url = (
        f"https://www.tiktok.com/v2/auth/authorize/?"
        f"client_key={CLIENT_KEY}"
        f"&response_type=code"
        f"&scope={SCOPES.replace(' ', '%20')}"
        f"&redirect_uri={REDIRECT_URI.replace(':', '%3A').replace('/', '%2F')}"
        f"&state=test123"
    )
    return redirect(oauth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Missing code", 400

    token_url = "https://open.tiktokapis.com/v2/oauth/token/"
    data = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(token_url, json=data, headers=headers)

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
