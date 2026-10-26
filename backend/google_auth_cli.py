from google_oauth import authorize,status
import argparse
p=argparse.ArgumentParser();p.add_argument('command',choices=['login','status'])
args=p.parse_args()
if args.command=='login':
    authorize(interactive=True)
    print('Authorized locally. Do not share your OAuth token.')
else: print(status())
