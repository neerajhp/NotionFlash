import requests
import json
import time
import os
from dotenv import load_dotenv
import notionservice.service as notionService
import ankiservice.service as ankiService
from ankiservice.ankiCard import ankiCard



#************** CONSTANTS **************#

DEBUG = False

# Load environment variables
load_dotenv()

#ANKI server properties
DECK = os.getenv("DECK")

#Connect to Notion
# API Endpoints and variables

PAGES = [{"pageID":os.getenv("DUMMY_PAGE_ID"), "cardTag": "dummy"}]


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

    #Open Anki
    os.system("open /Applications/Anki.app")

    for notionPage in PAGES: 
        pageBlocks = notionService.getAllPageBlocks(notionPage["pageID"])
        toggleLists = notionService.filterBlocks(pageBlocks, "toggle")
        #TODO filter toggleLists by last updated

        for toggle in toggleLists:
            #Get Question and Answer
            toggleQuestion = getQuestion(toggle)
            toggleAnswer = getAnswer(toggle)
            #Check if content contains image
            if ("image" in notionService.getContentTypes(toggleAnswer)) :
                images = notionService.getImages(toggleAnswer)
                for image in images:
                    #Download image(s) to anki
                    ankiService.downloadMedia(image[0], image[1])

            #Stringify notion content
            questionString = notionService.stringifyContent(toggleQuestion)
            answerString = notionService.stringifyContent(toggleAnswer)
            #Transform into ANKI payload
            newCard = ankiCard(DECK,  notionPage["cardTag"], questionString, answerString)
            # Add card 
            ankiService.addCard(newCard)



if __name__ == '__main__':
    PROFILER = False
    if PROFILER:
        import cProfile, pstats
        profiler = cProfile.Profile()
        profiler.enable()
        main()
        stats = pstats.Stats(profiler).sort_stats('ncalls')
        stats.print_stats()
    else:
        main()