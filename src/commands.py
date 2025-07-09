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
    if res.status_code != 200: return f"HTTP error: {HTTPStatus(res.status_code).phrase}."

    content = res.json()[0] # Get the JSON from the response and parse it as a python object, get the first item because everything is inside a list
    if "message" in content: return content["message"] # The error page has a message property containing the error message, so we return that from the json

def qotd():
    pass