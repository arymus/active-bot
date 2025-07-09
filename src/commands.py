import requests # For sending HTTP requests
from http import HTTPStatus # For printing HTTP status information

def get_fact():
    res = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random") # Send a GET request to the URL that generates random facts

    # If the status code is not 200 (an HTTP error occurred), return the HTTP status message
    if res.status_code != 200: return f"HTTP error: {HTTPStatus(res.status_code).phrase}."

    content = res.json() # Parse the data to JSON format
    return content["text"] # Extract the text from the JSON

def dictionary(word):
    res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.strip()}") # Send a GET request to the URL (word.strip() removes all whitespace)
    
    # If the status code is not 200 (an HTTP error occurred), return the HTTP status message
    if res.status_code != 200:
        if res.status_code == 404: return res.json()["message"] # If the status code is 404, it means the word doesn't exist. However, the API gives back a ["message"] property that we can return
        else: return f"HTTP error: {HTTPStatus(res.status_code).phrase}." # Since the above only occurs on 404 errors, any other error should just return the HTTP status

    content = res.json()[0] # Get the JSON from the response and parse it as a python object, get the first item because everything is inside a list
    """
    .join() is a method that joins lists or other strings together into one string.
    In this case, we're joining list(word.strip())[0].upper() + word.strip()[1:].
    list() separates a string into an array containing each letter.
    word.strip() removes all whitespace before and after the word.
    [0] gets the first letter because index 0 of a word as an array would be the first letter.
    .upper() translates that letter to uppercase
    word.strip()[1:] creates a copy of the word excluding its first letter (index 1 all the way to the end)

    We add the uppercase letter and the rest of the word to get the word with its first letter uppercased
    """
    formatted_word = "".join(list(word.strip())[0].upper() + word.strip()[1:]) # Get the word, but it's first letter is uppercase
    summary = f"## {formatted_word}\n" # A string containing the word and a line break, the double hash is markdown syntax for a subheader
    meanings = content["meanings"] # Get the meanings property in the JSON, which is an array containing all the meanings of the word

    # For each item in the ["meanings"] array, where the selected item is i
    for i in meanings:

        # i["partOfSpeech"] is a property from the ["definitons"] object inside meaning that contains the part of speech context of the definition
        formatted_partofspeech = "".join(list(i["partOfSpeech"].strip())[0].upper() + i["partOfSpeech"].strip()[1:]) # Get the part of speech but it's first letter is capitalized

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
        summary += f"**{formatted_partofspeech}**\n" # Get the part of speech of the word and add it to the summary with a break at the end. The double asterisk is markdown syntax for bold
        definitions = i["definitions"][:3] # Get the array in the ["definitions"] property, but reduce it to its first 3 items

        # For each item in the ["definitions"] array, where the selected item is j
        for j in definitions: summary += f"{j["definition"]}\n" # Get the definition of each meaning in the ["definitions"], and add it to summary with a line break at the end
        summary += "\n" # Add a break at the end of each part of speech context for formatting
    return summary

def qotd():
    pass