import requests # For sending HTTP requests
from http import HTTPStatus # For printing HTTP status information

def get_fact():
    res = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random") # Send a GET request to the URL that generates random facts

    # If the status code is not 200 (an HTTP error occurred), return the HTTP status message
    if res.status_code != 200: return f"HTTP error: {HTTPStatus(res.status_code).phrase}."

    content = res.json() # Parse the data to JSON format
    return content["text"] # Extract the text from the JSON