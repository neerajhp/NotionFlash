import logging
import ankiservice.api as ankiAPI

# Get logger
logger = logging.getLogger(__name__)


def downloadMedia(url, filename):
    ankiAPI.downloadMedia(url, filename)


def addCard(card):
    return ankiAPI.addCard(card)
