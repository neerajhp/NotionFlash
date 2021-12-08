import requests
from dotenv import load_dotenv
import os

#************** SETUP **************#
load_dotenv()

# API Endpoints and variables
# TODO figure out how to move to .env?
SECRET = os.getenv("NOTION_SECRET")
baseNotionURL = "https://api.notion.com/v1/blocks/"
HEADER = {"Authorization": SECRET, "Notion-Version":"2021-05-13", "Content-Type": "application/json"}


#************** API  **************#

def getBlocks(id, params={}):
    """ Gets children of Notion content block specified by ID. Limited to 100 results.
    
        Parameters:
            id (str): Notion Block ID
            params: 

        Returns:
            response (json[]): JSON array of block content.
    """
    try:
        response = requests.get(baseNotionURL + id + "/children", headers=HEADER, data={}, params=params)
        response.raise_for_status()
    #TODO Move to error handler
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

    return response.json()