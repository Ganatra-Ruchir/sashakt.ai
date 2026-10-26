"""Read-only Google Sheets and Drive connector with desktop OAuth."""
import re
from urllib.parse import urlparse,quote
from google.auth.transport.requests import AuthorizedSession
from google_oauth import authorize
def google_id(url,kind):
    raw=url.strip()
    if re.fullmatch(r'[\w-]{15,}',raw):return raw
    u=urlparse(raw)
    if u.scheme!='https' or u.hostname not in ('docs.google.com','drive.google.com'):raise ValueError('Invalid Google URL')
    pattern=r'/spreadsheets/d/([\w-]+)' if kind=='sheet' else r'/folders/([\w-]+)'
    match=re.search(pattern,u.path)
    if not match:raise ValueError('Invalid '+kind+' URL')
    return match.group(1)
def client():return AuthorizedSession(authorize(False))
def read_spreadsheet(url,max_rows=10000):
    sid=google_id(url,'sheet');s=client();base='https://sheets.googleapis.com/v4/spreadsheets/'+sid
    m=s.get(base,params={'fields':'spreadsheetId,properties/title,sheets/properties/title'},timeout=40);m.raise_for_status();meta=m.json()
    sheets={}
    for tab in meta.get('sheets',[]):
        title=tab['properties']['title'];safe=title.replace("'","''")
        response=s.get(base+'/values/'+quote("'"+safe+"'!A1:ZZ"+str(max_rows),safe='!'),timeout=40)
        response.raise_for_status();sheets[title]=response.json().get('values',[])
    return {'id':sid,'title':meta.get('properties',{}).get('title'),'url':'https://docs.google.com/spreadsheets/d/'+sid+'/edit','worksheets':sheets}
def discover_folder(url,limit=200):
    folder=google_id(url,'folder');s=client();items=[];token=None
    while len(items)<limit:
        params={'q':f"'{folder}' in parents and trashed=false and mimeType='application/vnd.google-apps.spreadsheet'",'fields':'nextPageToken,files(id,name,webViewLink,modifiedTime)','pageSize':min(100,limit-len(items)),'supportsAllDrives':'true','includeItemsFromAllDrives':'true'}
        if token:params['pageToken']=token
        r=s.get('https://www.googleapis.com/drive/v3/files',params=params,timeout=40);r.raise_for_status()
        result=r.json();items+=result.get('files',[]);token=result.get('nextPageToken')
        if not token:break
    return items
