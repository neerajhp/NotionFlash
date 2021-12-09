import notionservice.api as notionAPI


def getToggleHeader(toggle):
    """ Gets typed content within block.
    
        Parameters:
            id (str): Notion Block ID

        Returns:
            pageBlocks (json[]): JSON array of parent blocks on page.
    """
    return toggle["toggle"]["text"]

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
    blocks = {"has_more" : False, "start_cursor": None}
    params = {}
    pageBlocks = []
    
    while (getNext):

        # Get children of specified block/page specified by id 
        blocks = notionAPI.getBlocks(id, params)
       
        # Check if pagination required
        if blocks["has_more"]:
            params["start_cursor"] =  blocks["next_cursor"]
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
    
    for block in parentBlocks:
       blockContent = notionAPI.getBlocks(block["id"])
       pageContent += blockContent["results"]
    
    return pageContent