import requests


endpoint = "https://www.el-tiempo.net/api/json/v2/provincias/15"

def load_json():
    response = requests.get(endpoint)
    return response.json()

def extract_info(response):
    info_coruña = {}
    info_coruña["title"] = response["title"]
    info_coruña["hoy"] = response["today"] ["p"]
    info_coruña["cielo"] = response["ciudades"][0]["stateSky"]["description"]
    info_coruña["temp_max"] = response["ciudades"][0]["temperatures"]["max"]
    info_coruña["temp_min"] = response["ciudades"][0]["temperatures"]["min"]
    return info_coruña


response = load_json()
print(extract_info(response))