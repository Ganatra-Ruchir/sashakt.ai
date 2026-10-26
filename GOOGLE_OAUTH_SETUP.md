# Elixir Foundation Google Workspace OAuth (local only)

Use the extracted downloadable package for the complete backend. These repository files are a portable connector implementation, **not** a production-secured deployment.

1. Ask your organization's Google Workspace administrator to approve Drive/Sheets read access and the Cloud project.
2. Create a Google Cloud project under the appropriate organization. Enable the Google Drive API and Google Sheets API.
3. Configure Google Auth Platform. Use Internal audience only if the Cloud project belongs to the same Workspace organization; otherwise External testing and approved test users.
4. Create an OAuth Client of type **Desktop app**, download the JSON and put it at `%USERPROFILE%\.sashakt-ai\client_secret.json`. Never commit credentials.
5. Install `python -m pip install -r backend/requirements-oauth.txt`.
6. Run `python backend/google_auth_cli.py login`. Follow Google's local-browser OAuth consent flow.
7. Run `python backend/google_auth_cli.py status`.

The scopes are `drive.readonly` and `spreadsheets.readonly`; broad read-only permissions may require organization/admin approval and OAuth app verification for external rollout. Limit discovery to approved Sashakt folders. Keep refresh tokens and beneficiary data on the local machine. Do **not** expose the prototype backend directly over the public internet or connect it to public Vercel before authentication, per-user access control, audit logging, and secure transport are implemented.

Google references:
- https://developers.google.com/identity/protocols/oauth2/native-app
- https://developers.google.com/workspace/drive/api/quickstart/python
