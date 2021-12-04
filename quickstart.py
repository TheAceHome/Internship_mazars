from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.modify']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('drivers/token.json'):
        creds = Credentials.from_authorized_user_file('drivers/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'drivers/client.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('drivers/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service


def search_messages_unread(service):
    result = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=10).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=10).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages


def search_messages_inbox(service):
    result = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=10).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=10).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages


def get_lables(service):
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

service = main()

search_messages_unread(service)
result = service.users().messages().list(userId='me').execute()
messages = result.get('messages')

for message in search_messages_unread(service):
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            service.users().messages().modify(userId='me', id=message['id'], body={
                                            'removeLabelIds': ['UNREAD']}).execute()
            print(msg['snippet'])
