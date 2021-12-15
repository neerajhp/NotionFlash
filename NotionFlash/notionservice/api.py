import logging
import requests
from dotenv import load_dotenv
import os


# Get logger
logger = logging.getLogger(__name__)

#************** SETUP **************#
load_dotenv()

# API Endpoints and variables
# TODO figure out how to move to .env?
SECRET = os.getenv("NOTION_SECRET")
baseNotionURL = "https://api.notion.com/v1/blocks/"  # Should be v1
HEADER = {"Authorization": SECRET, "Notion-Version": "2021-05-13",
          "Content-Type": "application/json"}


#************** API  **************#

def getBlocks(id, params={}):
    """ Gets children of Notion content block specified by ID. Limited to 100 results.

        Parameters:
            id (str): Notion Block ID
            params: Optional argument used to specify starting block ID for pagination.

    """
    logger.debug("Requesting block children")

    try:
        response = requests.get(
            baseNotionURL + id + "/children", headers=HEADER, data={}, params=params)
        response.raise_for_status()
    # TODO Move to error handler

    except requests.exceptions.HTTPError as errh:
        logger.error("HTTPERROR:  There was an error connecting to Notion")
        pass
    except requests.exceptions.ConnectionError as errc:
        logger.error(errc)
        pass
    except requests.exceptions.Timeout as errt:
        logger.error(errt)
        pass
    except requests.exceptions.RequestException as err:
        logger.error(err)

    logger.debug("Request successful")
    return response.json()
