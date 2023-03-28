from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']


def get_credentials():
    """
    Retrieves the user's credentials from the 'token.json' file. If no valid credentials are found,
    it prompts the user to log in and authorizes the application. It then saves the credentials to the 
    'token.json' file for future use.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_unread_emails(service, number_of_mails):
    """
    Retrieves the specified number of unread emails from the user's inbox using the Gmail API.
    Returns a list of message IDs.
    """
    main_page = service.users().messages().list(userId='me',
                                                q='label:unread',
                                                maxResults=number_of_mails).execute()
    next_page_token = main_page.get('nextPageToken')
    next_page = service.users().messages().list(userId='me',
                                                q='label:unread',
                                                maxResults=number_of_mails,
                                                pageToken=next_page_token).execute()
    message_ids = [msg['id'] for msg in next_page['messages']]
    return message_ids


def delete_emails(service, message_ids):
    """
    Deletes the specified emails from the user's inbox using the Gmail API.
    Returns a dictionary containing information about the deleted messages.
    """
    try:
        response = service.users().messages().batchDelete(userId='me', body={'ids': message_ids}).execute()
        return response
    except HttpError as e:
        print(f"Error deleting messages: {e}")
        return None


def main():
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    number_of_mails = int(input("How many mails should be removed? ")) # max 500
    while not 0 < number_of_mails <= 500:
        number_of_mails = int(input("Minimum is 1, and maximum is 500 mails?"))
    print(f"You are removing {number_of_mails} unread mails from your inbox")

    message_ids = get_unread_emails(service, number_of_mails)
    print(f"Message IDs to delete: {message_ids}")

    response = delete_emails(service, message_ids)
    if response:
        print(f"Messages deleted: {response}")


if __name__ == '__main__':
    main()
