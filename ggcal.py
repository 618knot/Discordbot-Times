import datetime
import os.path
from googleapiclient.discovery import build
from google.auth import load_credentials_from_file


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def calendar_info3():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # Load credential file for service account
    creds = load_credentials_from_file(
        'cistlt-calendar.json', SCOPES
    )[0]

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    # NOTE: Set your calendar id
    events_result = service.events().list(calendarId='cist.lt.club@gmail.com', timeMin=now,
                                        maxResults=3, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    ret = []
    if not events:
        return -1
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        ret.append((start, event['summary']))

    return ret
print(calendar_info3())
