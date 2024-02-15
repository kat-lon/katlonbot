import requests
import os
from dotenv import load_dotenv

endpoint = "https://api.nasa.gov/planetary/apod?api_key="

def get_apikey():
    return os.getenv('APOD_API')

def load_json(api_key):
    response = requests.get(endpoint + api_key)
    return response.json()

def extract_info(response):
    apod = {}
    apod["title"] = response["title"]
    apod["descripcion"] = response["explanation"]
    apod["imagen"] = response["url"]
    return apod

api_key = get_apikey()
print(extract_info(load_json(api_key)))
