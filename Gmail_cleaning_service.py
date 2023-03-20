from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']


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

        # # Viser labels
        # request = service.users().labels().list(userId='me').execute()
        # for label in request['labels']:
        #     print(label['id'])

        number_of_mails = int(input("How many mails should be removed? ")) # max 500
        while not 0 < number_of_mails <= 500:
            number_of_mails = int(input("Minimum is 1, and maximum is 500 mails?"))
        print(f"You are removing {number_of_mails} unread mails from your inbox")

        # Makes sure you don't delete new mails
        main_page = service.users().messages().list(userId='me', 
                                                    q='label:unread', 
                                                    maxResults=number_of_mails).execute()
        next_page_token = main_page.get('nextPageToken')
        next_page = service.users().messages().list(userId='me', 
                                                    q='label:unread', 
                                                    maxResults=number_of_mails, 
                                                    pageToken=next_page_token).execute()

        besked_id = next_page['messages'][0]['id']
        specific_message = service.users().messages().get(userId='me', id=besked_id).execute()
        print(f"Message to remove: {specific_message['snippet']}")
        # trashing = service.users().messages().trash(userId='me', id=besked_id).execute()
        # print(f"Trashed message: {trashing}")


        # Get historyId
        # besked = service.users().messages().get(userId='me', id=besked_id, format='full').execute()
        # print(besked)
        # start_hist_id = f"{besked['historyId']}"
        # print(start_hist_id)
        # request = service.users().history().list(userId='me', startHistoryId=2625661).execute()
        # print(request)

        message_Ids = []
        for i in range(number_of_mails):
            message_Ids.append(str(next_page['messages'][i]['id']))
        Body = {'ids': message_Ids}
        print(Body)
        batch = service.users().messages().batchDelete(userId='me', body={'ids': message_Ids}).execute()
  
        # for at vise alle userIDs
        # count = 0
        # for i in range(number_of_mails):
        #     print("{i} user id: ".format(i=i+1) + messages['messages'][i]['id'])
        #     count += 1
        # print(count)

        # ------ tælle hvor mange sider der er -------
        # main_page = service.users().messages().list(userId='me', q='label:unread', maxResults=500).execute()
        # next_page_token = main_page.get('nextPageToken')
        # next_page = service.users().messages().list(userId='me', q='label:unread', maxResults=500, pageToken=next_page_token).execute()
        # count = 0
        # while True: 
        #     if not next_page_token:
        #         break
        #     main_page = next_page
        #     next_page_token = main_page['nextPageToken']
        #     next_page = service.users().messages().list(userId='me', q='label:unread', pageToken=next_page_token).execute()
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