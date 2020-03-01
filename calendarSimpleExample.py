from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    calendarList = service.calendarList().list().execute()

    #create an array for later use of calendarId
    calendarIds = []
    #populate calendarIds from the API
    for calendar in calendarList['items']:
        calendarIds.append(calendar['id'])

    #print the list of available calendarss
    i=1
    print("Choose a calendar to show events from it")
    for calendar in calendarList['items']:
        print(str(i) + ". " + calendar['summary'])
        i+=1

    #let the user choose the calendar
    userInput = int(input())

    #add time for printing purposes
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    #get the events and print them
    events = service.events().list(calendarId=calendarIds[userInput-1], timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    for event in events['items']:
        print(event['summary'] + " -----", str(event['start'].get('dateTime')))



    """
    the next item on the list is doing a UI.
    """
if __name__ == '__main__':
    main()
