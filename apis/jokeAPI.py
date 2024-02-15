import requests

endpoint = "https://v2.jokeapi.dev/joke/Dark?type=single"

def load_json():
    response = requests.get(endpoint)
    return response.json()

def extract_info(response):
    bromita = {}
    bromita["chiste"] = response["joke"]
    return bromita

print(extract_info(load_json()))