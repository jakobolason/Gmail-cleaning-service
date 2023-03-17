from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def main():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        
        results = service.users().labels().get(userId='me', id='UNREAD').execute()
        label_to_get = results.get('messagesTotal')
        labelIDs = ['UNREAD']
        messages = service.users().messages().list(userId='me', q='in:inbox is:unread', pageToken='2').execute()
        
        # for at vise alle userIDs
        # count = 0
        # for title in messages['messages']:
        #     for message in title.values():
        #         if count % 2 != 1:
        #             print("userID\t\t  ThreadID")
        #             print(message, end="  ")
        #         else:
        #             print(message, "\n")
        #         count += 1

        # ------ tælle hvor mange sider der er -------
        # main_page = service.users().messages().list(userId='me', q='in:inbox is:unread', maxResults=500).execute()
        # next_page_token = main_page.get('nextPageToken')
        # next_page = service.users().messages().list(userId='me', q='in:inbox is:unread', maxResults=500, pageToken=next_page_token).execute()
        # count = 0
        # while True: 
        #     if not next_page_token:
        #         break
        #     main_page = next_page
        #     next_page_token = main_page['nextPageToken']
        #     next_page = service.users().messages().list(userId='me', q='in:inbox is:unread', pageToken=next_page_token).execute()
        #     if 'nextPageToken' not in next_page:
        #         break
        #     count += 1
        # print(count)

        # -------- kigge på en besked ------
        # message_to_remove = messages['messages'][1]['id']
        # print(message_to_remove)
        # specific_message = service.users().messages().get(userId='me', id=message_to_remove).execute()
        # print(specific_message['snippet'])


    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()