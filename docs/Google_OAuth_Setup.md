# Google OAuth Setup Guide

To enable the Gmail integration, you need to create a project in the Google Cloud Console and generate OAuth credentials.

## Step 1: Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click on the project drop-down menu at the top of the page.
3. Click the **New Project** button.
4. Enter a project name (e.g., "Voice Controlled Gmail Assistant") and click **Create**.

## Step 2: Enable the Gmail API
1. Make sure your new project is selected.
2. Navigate to **APIs & Services > Library** from the left-hand menu.
3. Search for **Gmail API**.
4. Click on the Gmail API result and click **Enable**.

## Step 3: Configure the OAuth Consent Screen
1. Navigate to **APIs & Services > OAuth consent screen**.
2. Choose **External** (or Internal if you have a Google Workspace) and click **Create**.
3. Fill in the required fields:
   - **App name:** Voice Controlled Gmail Assistant
   - **User support email:** Your email address
   - **Developer contact information:** Your email address
4. Click **Save and Continue**.
5. On the **Scopes** page, click **Add or Remove Scopes**.
6. Add the following scopes:
   - `https://www.googleapis.com/auth/gmail.modify`
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/gmail.send`
   - `https://www.googleapis.com/auth/gmail.compose`
7. Click **Save and Continue**.
8. On the **Test users** page, add your own email address as a test user. Click **Save and Continue**.

## Step 4: Create OAuth Credentials
1. Navigate to **APIs & Services > Credentials**.
2. Click **Create Credentials > OAuth client ID**.
3. Select **Desktop app** (for local backend-driven auth) or **Web application**. For this implementation, select **Web application**.
4. Set the **Name** to "React Frontend".
5. Under **Authorized redirect URIs**, add:
   - `http://localhost:5173/auth/callback`
   - `http://localhost:8000/auth/callback`
   - `http://localhost:5173`
   - `http://localhost:8000`
6. Click **Create**.
7. Download the JSON file by clicking **Download JSON**.

## Step 5: Save Credentials
1. Rename the downloaded file to `credentials.json`.
2. Place this file precisely at `/home/crdy/testing/SE_lab/APP/backend/credentials.json`.

Once this is complete, the backend will be able to read the credentials and authenticate users.
