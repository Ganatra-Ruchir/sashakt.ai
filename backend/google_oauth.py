"""Desktop OAuth token management. Run authorization only from a local command line."""
import os
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
SCOPES=['https://www.googleapis.com/auth/drive.readonly','https://www.googleapis.com/auth/spreadsheets.readonly']
def private_dir():
    return Path(os.getenv('SASHAKT_PRIVATE_DIR',str(Path.home()/'.sashakt-ai'))).expanduser().resolve()
def authorize(interactive=False):
    token=private_dir()/'google_token.json'
    creds=Credentials.from_authorized_user_file(str(token),SCOPES) if token.exists() else None
    if creds and creds.valid:return creds
    if creds and creds.expired and creds.refresh_token:
        try:creds.refresh(Request())
        except RefreshError:
            if not interactive:raise RuntimeError('Google authorization revoked. Run local login again.')
            creds=None
    elif not interactive:raise RuntimeError('Run python backend/google_auth_cli.py login locally first.')
    if not creds or not creds.valid:
        if not interactive:raise RuntimeError('Run local Google authorization again.')
        from google_auth_oauthlib.flow import InstalledAppFlow
        client=Path(os.getenv('GOOGLE_OAUTH_CLIENT_FILE',str(private_dir()/'client_secret.json')))
        if not client.is_file():raise FileNotFoundError('Missing private Google Desktop OAuth client file')
        flow=InstalledAppFlow.from_client_secrets_file(str(client),SCOPES)
        creds=flow.run_local_server(host='127.0.0.1',port=0,open_browser=True)
    token.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
    token.write_text(creds.to_json(),encoding='utf-8')
    try:os.chmod(token,0o600)
    except OSError:pass
    return creds
def status():
    return {'configured':(private_dir()/'client_secret.json').is_file(),'authorized':(private_dir()/'google_token.json').is_file()}
