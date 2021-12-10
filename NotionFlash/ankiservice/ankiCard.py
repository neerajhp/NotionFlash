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

    def addContent(self, question, answer):
        """ Add question and answer content to card.

            Parameters:
                question (str): Question to go on front of Anki card.
                answer (str): Answer to go on back of Anki card.

        """
        self.payload["note"]["fields"]["Front"] = question
        self.payload["note"]["fields"]["Back"] = answer