import notionservice.api as notionAPI
import logging

# Get logger
logger = logging.getLogger(__name__)


def getToggleHeader(toggle):
    """ Gets toggle header

        Parameters:
            id (str): Notion Block ID

        Returns:
            pageBlocks (json[]): JSON array of parent blocks on page.
    """
    # TODO Need more comprehensive testing
    # LOG
    logger.debug("Getting header of toggle")
    return toggle['toggle']['text']


def getToggleBody(toggle):
    """ Gets nested content of notion toggle.

        Parameters:
            toggle (JSON[]): Notion JSON Block

        Returns:
            Notion JSON payload of content
    """
    # LOG
    logger.debug("Getting body of toggle")
    return notionAPI.getBlocks(toggle['id'])['results']


def getPageRootBlocks(id):
    """ Gets all root blocks on a specified Notion page.

        Parameters:
            id (str): Notion Block OR Page ID

        Returns:
            pageBlocks (JSON[]): JSON array of parent blocks on page.
    """
    # Initial values
    getNext = True
    blocks = {"has_more": False, "start_cursor": None}
    params = {}
    pageBlocks = []

    # LOG
    logger.debug("Requesting blocks from page...")

    while (getNext):

        # Get children of specified page specified by id
        blocks = notionAPI.getBlocks(id, params)

        # Check if pagination required
        if blocks["has_more"]:
            logger.debug("Requesting more blocks from page...")
            params["start_cursor"] = blocks["next_cursor"]
            getNext = True
        else:
            getNext = False

        pageBlocks += blocks["results"]

    logger.debug("Got %d blocks from page" % len(pageBlocks))

    return pageBlocks


def filterBlocks(content, filter):
    """ Filter JSON array (formatted as Notion Payload) by type of block.

        Parameters:
            content (json[]): JSON array of notion blocks
            filter (str): content type

        Returns:
            JSON array of filtered content.
    """
    # LOG
    logger.debug("Filtering content of type: %s" % filter)

    return [block for block in content if block['type'] == filter]


def getAllPageBlocks(pageID):
    """ Recursively gets all nested blocks of Notion page specified by id.

        Parameters:
            id (str): Notion Page ID

        Returns:
            pageContent (json[]): JSON array of page content.
    """

    logger.debug("Requesting blocks from page...")
    pageContent = getPageRootBlocks(pageID)
    for block in pageContent:
        if block["has_children"]:
            blockContent = notionAPI.getBlocks(block["id"])["results"]
            pageContent += blockContent

    return pageContent


def parseToHTML(contentArray):
    """ Parse notion rich text to html.

        Parameters:
            content (json[]): JSON array of typed content


        Returns:
            string (str): Stringified content
    """
    # LOG
    logger.debug("Attempting to parse Notion rich text content to html")

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


def stringifyContent(content):
    """ Convert notion text content to string .

        Parameters:
            content (json[]): JSON array of typed content


        Returns:
            string (str): Stringified content
    """
    # LOG
    logger.debug("Stringifying Notion content")

    string = ""

    for item in content:

        if item["type"] == "text":
            string += parseToHTML([item])

        elif item["type"] == "paragraph":
            string += parseToHTML(item["paragraph"]["text"])

        elif item["type"] == "bulleted_list_item":
            # Format bulleted Llst
            string += "<ul><li>" + \
                parseToHTML(item["bulleted_list_item"]["text"]) + "</li></ul>"

        elif item["type"] == "numbered_list_item":
            # Format numbered list
            if string.endswith("</ol>\n"):
                string = string.replace("</ol>\n", "")
                string += "<li>" + \
                    parseToHTML(item["numbered_list_item"]
                                ["text"]) + "</li></ol>"
            else:
                string += "<ol><li>" + \
                    parseToHTML(item["numbered_list_item"]
                                ["text"]) + "</li></ol>"
        elif item["type"] == "image":
            filename = item['id'] + ".png"
            # Add image to body
            string += "<br><img src='" + filename + "'>"

        # Add break in string
        string += '\n'

    return string


def getImages(content):
    """ Gets all images in notion content body .

        Parameters:
            content (json[]): JSON array of typed content


        Returns:
            images ([str, str]): List of (url, filename) tuple for each image found
    """
    # LOG
    logger.debug("Getting images from Notion content body")

    images = []
    for item in content:
        if item["type"] == "image":
            url = item["image"]["file"]["url"]
            filename = item['id'] + ".png"
            images.append((url, filename))
            # Add image to body
    return images


def getContentTypes(content):
    """ Returns list of content types in block of Notion content .

        Parameters:
            content (json[]): JSON array of typed content


        Returns:
            List of content types.
    """
    logger.debug("Getting content types of Notion content")
    return [item["type"] for item in content]
