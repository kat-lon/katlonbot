import pandas as pd

def convert_to_dataframe(archivo):
    return pd.read_csv(archivo) if archivo[-1:-4] == "csv" else pd.read_json(archivo)

def json_to_csv(dataframe):
    return dataframe.to_csv()

def csv_to_json(dataframe):
    return dataframe.to_json()

def get_csv_info(archivo_csv):
    return archivo_csv.info()