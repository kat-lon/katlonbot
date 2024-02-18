import pandas as pd
import json
import io

def convert_to_dataframe(archivo):
    return pd.read_csv(archivo) if archivo.endswith("csv") else pd.read_json(archivo)

def json_to_csv(dataframe, ruta):
    nueva_ruta = ruta[:-4] + "csv"
    dataframe.to_csv(nueva_ruta)
    return nueva_ruta

def csv_to_json(dataframe, ruta):
    nueva_ruta = ruta[:-3] + "json"
    dataframe.to_json(nueva_ruta, indent=4)
    return nueva_ruta

def get_csv_info(archivo_csv):
    buffer = io.StringIO()
    archivo_csv.info(buf=buffer)
    info = buffer.getvalue()
    return info