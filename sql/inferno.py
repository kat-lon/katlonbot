import mysql.connector

import os
from dotenv import load_dotenv

load_dotenv()
PASS = os.getenv('SQL_PWD')

def chamando_a_satanas():
    # Establece los detalles de conexión
    config = {
      'user': 'Iago',
      'password': PASS,
      'host': '193.144.42.124',
      'port': 33306,
      'database': 'inferno',
      'raise_on_warnings': True
    }

    # Conecta con la base de datos
    try:
        conn = mysql.connector.connect(**config)

        if conn.is_connected():
            QUERY = "select * from admision where nome = 'Iago'"

            cursor = conn.cursor()
            cursor.execute(QUERY)
            respuesta = cursor.fetchall()

            return respuesta[0]

    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")

    finally:
        # Cierra la conexión
        if 'conn' in locals() and conn.is_connected():
            conn.close()