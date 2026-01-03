# Deployment Guide: Syllabus Scraper

This guide will help you deploy your **Syllabus Scraper** application to the web so your friends can use it. We will use **Streamlit Community Cloud**, which is free and optimized for Streamlit apps.

## Prerequisites
- A [GitHub](https://github.com/) account.
- A [Streamlit Community Cloud](https://share.streamlit.io/) account (you can sign in with GitHub).

## Step 1: Push to GitHub

I have already initialized the git repository and committed your code locally. You just need to push it to a new remote repository.

1.  **Create a new repository** on GitHub:
    - Go to [github.com/new](https://github.com/new).
    - Name it `syllabus-scraper` (or whatever you prefer).
    - **Important**: You can make it **Public** or **Private**. If Private, only you can see the code, but Streamlit Cloud can still deploy it.
    - Do **not** initialize with README, .gitignore, or license (we already have them).
    - Click **Create repository**.

2.  **Push your code**:
    - Copy the commands under "**…or push an existing repository from the command line**". They should look like this (replace `YOUR_USERNAME` with your actual GitHub username):
      ```bash
      git push -u origin main
      ```
    - Run these commands in your terminal.

## Step 2: Deploy to Streamlit Cloud

1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **New app**.
3.  Select your new repository (`syllabus-scraper`) from the expected dropdown.
4.  It should auto-detect:
    - **Branch**: `main`
    - **Main file path**: `app.py`
5.  Click **Deploy!** 🚀

## Step 3: Configure Secrets (Crucial!)

Your app needs the `GEMINI_API_KEY` to work. Since we (correctly) ignored the `.env` file so your secrets aren't public on GitHub, you need to add this key to Streamlit Cloud manually.

1.  On your deployed app dashboard, click the **Settings** menu (three dots in the top right) or "Manage app" in the bottom right.
2.  Go to **Settings** -> **Secrets**.
3.  Paste your API key in the TOML format:
    ```toml
    GEMINI_API_KEY = "your-actual-api-key-starting-with-AIza..."
    ```
4.  Click **Save**.

## Done!
Your app should now be live! You can share the URL (e.g., `https://syllabus-scraper.streamlit.app`) with your friends.
