import requests
import json
import time
import os
from dotenv import load_dotenv
from pathlib import Path



#************** CONSTANTS **************#

DEBUG = False

# Load environment variables
load_dotenv()

#ANKI server properties
ankiServerURL = "http://127.0.0.1:8765/"
DECK = os.getenv("DECK")

#Connect to Notion
# API Endpoints and variables
SECRET = os.getenv("NOTION_SECRET")
baseNotionURL = "https://api.notion.com/v1/blocks/"
HEADER = {"Authorization": SECRET, "Notion-Version":"2021-05-13", "Content-Type": "application/json"}
DATABASES = [{"Database":os.getenv("AWS_ID"), "cardTag": "AWS"}]




#************** HELPERS **************# 

def getNotionPage(id):
    """Notion API to get blocks from page. Limited to 100 results"""
    getPage = True
    responseJSON = {"has_more" : False, "start_cursor": None}
    pageContent = []
    params = {}

    while (getPage):

        try:
            response = requests.get(baseNotionURL + id + "/children", headers=HEADER, data={}, params=params)
            responseJSON = response.json()
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("There was an error with Notion")
            pass
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            pass
        except requests.exceptions.Timeout as errt:
            print(errt)
            pass
        except requests.exceptions.RequestException as err:
            print(err)
            pass
       

        # Check for pagination
        if responseJSON["has_more"]:
            params["start_cursor"] =  responseJSON["next_cursor"]
            getPage = True
        else:
            getPage = False
                
        x = responseJSON
        pageContent += responseJSON["results"]
    
    return pageContent


def stringFormatter(contentArray):
    """Transform Notion rich text into html for ANKI"""
    string = ""
    for content in contentArray:
        if content["annotations"]["bold"]:
            string += "<b>" + content["plain_text"] + "</b>"
        elif content["annotations"]["italic"]:
            string += "<i>" + content["plain_text"] + "</i>"
        elif content["annotations"]["code"]:
            string += "<code>" + content["plain_text"] + "</code>"
        else: 
            string += content["plain_text"]
        
    return string

def downloadMedia(url, filename):
    """ ANKI api request to download media. Filename is usually block-id from notion concatenated with file type."""
    payload =  {
        "action": "storeMediaFile",
        "params": {
          "filename": filename ,
          "url": url
        }
    }
    response = requests.post(ankiServerURL, json=payload).json()
    if len(response) != 2:
        print('response has an unexpected number of fields')
    if 'error' not in response:
        print('response is missing required error field')
    if 'result' not in response:
        print('response is missing required result field')
    
    return response
   


def createPayload(question, answer, tag):
    """ Convert Notion data to  ANKI JSON payload. Only body is formatted. String formatting is handled by the stringFormatter function. """
    payload = {
    "action": "addNote",
    "version": 6,
    "params": {
        "note": {
            "deckName": DECK,
            "modelName": "Basic",
            "fields": {
                "Front": "",
                "Back": ""
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": DECK,
                    "checkChildren": False,
                    "checkAllModels": False
                }
            },
            "tags": [
                tag
            ],}
    }
    }
    body = ""
    cardFront = payload["params"]["note"]["fields"]["Front"]
    cardBack = payload["params"]["note"]["fields"]["Back"]

    #Update Question
    payload["params"]["note"]["fields"]["Front"] = stringFormatter(question)
   

    for content in answer:
        if content["type"] == "paragraph":
            body += stringFormatter(content["paragraph"]["text"])
        elif content["type"] == "bulleted_list_item":
            #Format bulleted List
            body += "<ul><li>" + stringFormatter(content["bulleted_list_item"]["text"]) + "</li></ul>"
        elif content["type"] == "numbered_list_item":
            #Format bulleted List
            if body.endswith("</ol>\n"):
                body = body.replace("</ol>\n", "")
                body += "<li>" + stringFormatter(content["numbered_list_item"]["text"]) + "</li></ol>"
            else:
                body += "<ol><li>" + stringFormatter(content["numbered_list_item"]["text"]) + "</li></ol>"
       
        elif content["type"] == "image":
            # Download Image to Anki Storage
            filename = content['id'] + ".png"
            downloadMedia(content["image"]["file"]["url"], filename )
            # Add image to body
            body += "<br><img src='" + filename + "'>"
            
            
        # Add break in body
        body += '\n'

    # Add to payload
    payload["params"]["note"]["fields"]["Back"] += body  + '\n'

    return payload

def createCard(payload):
    """ ANKI api request to add card to deck """
    response = requests.post(ankiServerURL, json=payload).json()
    if len(response) != 2:
        print('response has an unexpected number of fields')
    if 'error' not in response:
        print('response is missing required error field')
    if 'result' not in response:
        print('response is missing required result field')
    
    return response

#************** MAIN **************#

def main():
    if DEBUG:
        __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
        f = open(os.path.join(__location__, "./output.txt"), "w")


    # Open Anki
    os.system("open /Applications/Anki.app")

    for notionPage in DATABASES: 

        #Get Notion Page
        response = getNotionPage(notionPage["Database"])
        pageContent = response
        

        # Recursively get all page content
        for block in pageContent:
            if block['has_children'] == True:
                try:
                    response = requests.get(baseNotionURL + block['id'] + "/children", headers=HEADER, data={})
                    response.raise_for_status()
                    pageContent += response.json()["results"]
                except requests.exceptions.HTTPError as errh:
                    print(errh)
                    pass
                except requests.exceptions.ConnectionError as errc:
                    print(errc)
                    pass
                except requests.exceptions.Timeout as errt:
                    print(errt)
                    pass
                except requests.exceptions.RequestException as err:
                    print(err)
                    pass

        # Filter toggle content 
        toggleContent = [block for block in pageContent if block['type'] == 'toggle']
        print("Successfully got toggle lists from " + notionPage["cardTag"] + " page on Notion.")

        #Anki properties to report
        totalCards = len(toggleContent)
        duplicateCards = 0
        newCards = 0
        cardsAdded = []


        #Convert toggle lists to JSON payload
        for toggle in toggleContent:
            #Get toggle header (the question)
            toggleQuestion = toggle["toggle"]["text"]
            try:
                #Get toggle body (the answer)
                response = requests.get(baseNotionURL + toggle['id'] + "/children", headers=HEADER, data={}).json()
                #Format body content into valid ANKI payload
                toggleAnswer = response["results"]
                #Create ANKI Payload
                newCard = createPayload(toggleQuestion, toggleAnswer, notionPage["cardTag"])
                #Post to ANKI server
                ankiResponse = createCard(newCard)
                if ankiResponse['error'] is not None:
                    duplicateCards += 1
                else:
                    newCards += 1
                    cardsAdded.append([newCard["params"]["note"]["fields"]["Front"] ,newCard["params"]["note"]["fields"]["Back"]])
                    
                if DEBUG:
                    f.write(newCard["params"]["note"]["fields"]["Front"] + "\n" + newCard["params"]["note"]["fields"]["Back"])
                    json.dump(newCard, f)
                    f.write("\n\n")
                
            except requests.exceptions.HTTPError as errh:
                    print(errh)
                    pass
            except requests.exceptions.ConnectionError as errc:
                    print("Connecton Refused")
                    time.sleep(2)
                    pass
            except requests.exceptions.Timeout as errt:
                    print(errt)
                    pass
            except requests.exceptions.RequestException as err:
                    print(err)
                    pass
            
        print("\n" + notionPage["cardTag"] + " tags done.\n")
        print("\tTotal number of toggles detected: " + str(totalCards))
        print("\tNumber of duplicate cards: " + str(duplicateCards) )
        print("\tNumber of new cards: " + str(newCards) )
        if len(cardsAdded) > 0:
            print("\tCards Added: ")
            for card in cardsAdded:
                print("\n\n\t" + card[0] + "\n\t" + card[1])

    print("\nALL DONE!\n")

    if DEBUG:
        f.close()
    # # Close Anki
    # os.system("pkill Anki")


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