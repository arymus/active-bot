from http import HTTPStatus
import requests

def dictionary(word):
    res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.strip()}") # Send a GET request to the URL (word.strip() removes all whitespace)
    
    # If the status code is not 200 (an HTTP error occurred), return the HTTP status message
    if res.status_code != 200: return f"HTTP error: {HTTPStatus(res.status_code).phrase}."

    content = res.json()[0] # Get the JSON from the response and parse it as a python object, get the first item because everything is inside a list

    # The error page has a message property containing the error message, so we return that from the JSON if it exists
    if "message" in content: return content["message"]

    summary = "" # An empty f-string to contain word data
    meanings = content["meanings"] # Get the meanings property in the JSON, which is an array containing all the meanings of the word

    # For each item in the ["meanings"] array, where the selected item is i
    for i in meanings:

        """
        The JSON has a specific format that we have to follow in order to correctly access data.
        First, there's an array that contains all the information (word name, audio, licenses, sources, etc.).
        Next, there's the ["meanings"] property that contains an array where each item has data for a different part of speech (like if a word has noun contexts and verb contexts).
        ex.
            Color; noun: The spectral composition of visible light.
            Color; verb: To give something color.
        Color has both noun and verb meanings, so ["meanings"] separates the different contexts for each part of speech.

        Inside the items in ["meanings"], there is ["partOfSpeech"] (contains the part of speech), and ["definitions"].
        ["definitions"] is an array containing all of the definitions under that part of speech context.

        Inside the items in ["definitions"], you have ["definition"], ["synonym"], ["antonym"], and ["example"].
        This is where we need to access for each word.
        """
        summary += i["partOfSpeech"] # Get the part of speech of the word from its section and add it to the summary
        definitions = i["definitions"][:3] # Get the array in the ["definitions"] property, but reduce it to its first 3 items

        # For each item in the ["definitions"] array, where the selected item is j
        for j in definitions: summary += j["definition"] # Get the definition of each meaning in the ["definitions"] array

    return summary