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
    #Como info no devuelve un string, sino que imprime la información directamente, 
    #crearemos un buffer para que escriba en el la salida y así poder recuperarla con
    #get_values. Despúes la parsearemos y la retornamos 
    buffer = io.StringIO()
    archivo_csv.info(buf=buffer)
    info_output = buffer.getvalue().splitlines()[2:-2]
    info_output = "\n".join([line.rstrip() for line in info_output])
    estadisticas = str(archivo_csv.describe())
    return info_output, estadisticas