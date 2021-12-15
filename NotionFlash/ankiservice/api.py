import logging
import json
import requests
from urllib.request import urlopen, Request


#************** SETUP **************#

# Get logger
logger = logging.getLogger(__name__)

# API Endpoints and variables
# TODO figure out how to move to .env?
ANK_SERVER_URL = 'http://localhost:8765'

#**************  API  **************#


def addCard(card):
    """  ANKI api request to download media.

    Parameters:
        card (ankiCard): Card to be added to

    Returns:
        1 if card succesfully added.
        0 if card already exists in deck.
        -1 if there was an error adding card.
    """
    payload = {
        "action": "addNote",
        "version": 6,
        "params": card.payload
    }

    logger.debug("Attempting to add card to Anki")
    # Attempt to post card
    response = requests.post(ANK_SERVER_URL, json=payload).json()
    # Check response for errors
    errMsg = errCheck(response)

    # Handle error message
    if (errMsg):
        if (errMsg == "cannot create note because it is a duplicate"):
            return 0
        else:
            logger.error("Could not add card : %s" % errMsg)
            return -1

    return 1


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
    errMsg = errCheck(response)

    if response == filename:
        logger.error("Media with that filename already exists locally.")
        return response
    if (errMsg):
        logger.error("Could not add media file : %s" % errMsg)

    return response


def errCheck(response):
    """  Checks errors in response from Anki connect and returns appropriate message

    Parameters:
        response (JSON): URL where media is located

    Returns:
        False if no error.
        Error message string otherwise.
    """

    if len(response) != 2:
        return'response has an unexpected number of fields'
    if 'error' not in response:
        return 'response is missing required error field'
    if 'result' not in response:
        return 'response is missing required result field'
    if response["error"] != None:
        return response["error"]
    return False
