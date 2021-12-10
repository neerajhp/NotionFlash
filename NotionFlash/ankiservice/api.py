import json
import requests
from urllib.request import urlopen, Request

#************** SETUP **************#


# API Endpoints and variables
# TODO figure out how to move to .env?
ANK_SERVER_URL = 'http://localhost:8765'

#**************  API  **************#


def addCard(card):
    """  ANKI api request to download media.

    Parameters:
        card (ankiCard): Card to be added to


    Returns:
        response: ANKIConnect response message
    """
    payload = {
        "action": "addNote",
        "version": 6,
        "params": card.payload
    }
    print
    # TODO move to error handler
    response = requests.post(ANK_SERVER_URL, json=payload).json()
    print(response["error"])
    if len(response) != 2:
        print('response has an unexpected number of fields')
    if 'error' not in response:
        print('response is missing required error field')
    if 'result' not in response:
        print('response is missing required result field')

    return response


def downloadMedia(url, filename):
    """  ANKI api request to download media.

    Parameters:
        url (str): URL where media is located
        filename (str): Filename to store media under. Usually block-id from notion concatenated with file type


    Returns:
        response: ANKIConnect response message
    """

    payload = {
        "action": "storeMediaFile",
        "params": {
            "filename": filename,
            "url": url
        }
    }
    response = requests.post(ANK_SERVER_URL, json=payload).json()
    # TODO Move to error handler
    if response == filename:
        print("Media with that filename already exists locally.")
        return response
    if len(response) != 2:
        print('response has an unexpected number of fields')
    if 'error' not in response:
        print('response is missing required error field')
    if 'result' not in response:
        print('response is missing required result field')

    return response
