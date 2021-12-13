import logging
import logging.config
import os
from dotenv import load_dotenv
import notionservice.service as notionService
import ankiservice.service as ankiService
from ankiservice.ankiCard import ankiCard


#************** CONSTANTS **************#

DEBUG = False

# Load environment variables
load_dotenv()

# ANKI server properties
DECK = os.getenv("DECK")

# Connect to Notion
# API Endpoints and variables

PAGES = [{"pageID": os.getenv("DUMMY_PAGE_ID"), "cardTag": "dummy"}]


#************** HELPERS **************#

def getQuestion(toggle):
    return notionService.getToggleHeader(toggle)


def getAnswer(toggle):
    return notionService.getToggleBody(toggle)

#************** MAIN **************#


def main():

    if DEBUG:
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        f = open(os.path.join(__location__, "./output.txt"), "w")

    # Open Anki
    os.system("open /Applications/Anki.app")

    for notionPage in PAGES:
        logger.debug("Connecting to " +
                     notionPage["cardTag"] + " page on Notion")
        pageBlocks = notionService.getAllPageBlocks(notionPage["pageID"])
        toggleLists = notionService.filterBlocks(pageBlocks, "toggle")
        logger.info("Successfully collected %d toggle lists from %s" %
                    (len(toggleLists), notionPage["cardTag"]))
        # TODO filter toggleLists by last updated

        for toggle in toggleLists:
            # Get Question and Answer
            logger.debug("Transforming toggle into Anki card")
            toggleQuestion = getQuestion(toggle)
            toggleAnswer = getAnswer(toggle)
            # Check if content contains image
            if ("image" in notionService.getContentTypes(toggleAnswer)):
                images = notionService.getImages(toggleAnswer)
                for image in images:
                    # Download image(s) to anki
                    ankiService.downloadMedia(image[0], image[1])

            # Stringify notion content
            questionString = notionService.stringifyContent(toggleQuestion)
            answerString = notionService.stringifyContent(toggleAnswer)
            # Transform into ANKI payload
            newCard = ankiCard(
                DECK,  notionPage["cardTag"], questionString, answerString)
            # Add card
            ankiService.addCard(newCard)


if __name__ == '__main__':
    logging.config.fileConfig(fname="./logs/logging.conf",
                              disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    logger.info("Let's Begin")

    main()
