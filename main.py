from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import graph_finviz
import time
import smtplib
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mimetypes import MimeTypes
import base64

##Create custom exeprions
class MyException(Exception):
    pass

sample_text1='Произошла ошибка, проверьте написание тикера. Обращаем внимание, что письмо пишется оп шаблону Ticker: AAPL competitors: 10'

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify','https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/gmail.compose','https://mail.google.com/']


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
    messages = []
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
    messages = []
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


def create_message(to, message_text):

  message = MIMEMultipart()
  message['to'] = to
  message['subject'] = 'ERROR'
  message.attach(MIMEText(message_text, 'plain'))
  return {'raw':base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, message):
  try:
    message = (service.users().messages().send(userId='me', body=message) .execute())
    print('Message Id: %s' % message['id'])
    return message
  except (errors.HttpError, error):
    print('An error occurred: %s' % error)


def create_message_with_attachment(to, ticker, message_text, files):

  message = MIMEMultipart()
  message['to'] = to
  message['subject'] = ticker

  msg = MIMEText(message_text)
  message.attach(msg)

  for i in files:
      mimetypes = MimeTypes()
      content_type, encoding = mimetypes.guess_type(i)
      if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
      main_type, sub_type = content_type.split('/', 1)
      if main_type == 'image':
        fp = open(i, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
      else:
        fp = open(i, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
      filename = os.path.basename(i)
      msg.add_header('Content-Disposition', 'attachment', filename=filename)
      message.attach(msg)

  return {'raw':base64.urlsafe_b64encode(message.as_bytes()).decode()}




if __name__ == "__main__":
    service = main()
    k=1
    while k==1:
        messages = search_messages_unread(service)
        for message in messages:
            try:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                service.users().messages().modify(userId='me', id=message['id'], body={
                    'removeLabelIds': ['UNREAD']}).execute()
                ticker = msg['snippet'].split(' ')[1]
                n = int(msg['snippet'].split(' ')[3])
                if graph_finviz.get_graph(ticker,n)==False:
                    raise Exception

                email_from = msg['payload']['headers'][7]['value'].replace('<','').replace('>','')
                msgt = create_message_with_attachment(email_from, ticker, 'text', ['screenshots/'+ticker+'.png','data.csv','data_with_mean.csv'])
                send_message(service,  msgt)

            except:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                email_from = msg['payload']['headers'][7]['value'].replace('<', '').replace('>', '')
                msgt = create_message(email_from, sample_text1)
                send_message(service, msgt)

        time.sleep(5)




