class ankiCard:
    """ 
    A class to represent an Anki Flash Card.
    Attributes
    ----------
    payload : JSON[]
        JSON payload for sending card via AnkiConnect

    Methods
    -------
    addContent(question, answer):
        Adds question and answer to 
    """

    def __init__(self, deck, tag, question, answer) -> None:
        self.payload = {
            "note": {
                "deckName": deck,
                "modelName": "Basic",
                "fields": {
                    "Front": "",
                    "Back": ""
                },
                "options": {
                    "allowDuplicate": False,
                    "duplicateScope": "deck",
                    "duplicateScopeOptions": {
                        "deckName": deck,
                        "checkChildren": False,
                        "checkAllModels": False
                    }
                },
                "tags": [
                    tag
                ],
            }
        }
        
        self.addContent(question, answer)


    

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
    


    def addContent(self, question, answer):
       
        self.payload["note"]["fields"]["Front"] = question
        self.payload["note"]["fields"]["Back"] = answer

        