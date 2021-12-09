import notionservice.api as notionAPI


def getToggleHeader(toggle):
    """ Gets toggle header

        Parameters:
            id (str): Notion Block ID

        Returns:
            pageBlocks (json[]): JSON array of parent blocks on page.
    """
    #TODO Need more comprehensive testing
    return toggle['toggle']['text']


def getToggleBody(toggle):
    """ Gets nested content of notion toggle.

        Parameters:
            toggle (JSON[]): Notion JSON Block

        Returns:
            Notion JSON payload of content
    """
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

    while (getNext):

        # Get children of specified block/page specified by id
        blocks = notionAPI.getBlocks(id, params)

        # Check if pagination required
        if blocks["has_more"]:
            params["start_cursor"] = blocks["next_cursor"]
            getNext = True
        else:
            getNext = False

        pageBlocks += blocks["results"]

    return pageBlocks


def filterBlocks(content, filter):
    """ Filter JSON array (formatted as Notion Payload) by type of block.

        Parameters:
            content (json[]): JSON array of notion blocks
            filter (str): content type

        Returns:
            JSON array of filtered content.
    """
    return [block for block in content if block['type'] == filter]


def getAllPageBlocks(pageID):
    """ Recursively gets all nested blocks of Notion page specified by id.

        Parameters:
            id (str): Notion Page ID

        Returns:
            pageContent (json[]): JSON array of page content.
    """
    pageContent = []
    parentBlocks = getPageRootBlocks(pageID)

    #BUG: If parent block is toggle then content returned is only toggle answer
    for block in parentBlocks:
       blockContent = notionAPI.getBlocks(block["id"])
       pageContent += blockContent["results"]

    return pageContent


def parseToHTML(contentArray):
    """ Parse notion rich text to html.

        Parameters:
            content (json[]): JSON array of typed content


        Returns:
            string (str): Stringified content
    """

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
    return [item["type"] for item in content ]