import notionservice.api as notionAPI

def getPageRootBlocks(id):
    """ Gets all root blocks on a specified Notion page.
    
        Parameters:
            id (str): Notion Block OR Page ID

        Returns:
            pageBlocks (json[]): JSON array of parent blocks on page.
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

def filterContent(content, filter):
    """ Filter JSON array (formatted as Notion Payload) by content type.
        
        Parameters:
            content (json[]): JSON array of notion content
            filter (str): content type 

        Returns:
            JSON array of filtered content.
    """
    return [block for block in content if block['type'] == filter]


def getPageContent(pageID):
    """ Recursively gets all nested content of Notion page specified by id.
        
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