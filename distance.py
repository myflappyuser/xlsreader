import os
from dotenv import load_dotenv
import googlemaps
from datetime import datetime

#Carga las variables del entorno
load_dotenv()

#Obtiene la API key
api_key = os.getenv("GOOGLE_MAPS_API_KEY")

def calcular_distancia_carretera(origen, destino, api_key):
    #Inicializando el cliente de Google maps
    gmaps = googlemaps.Client(key=api_key)

    #Realizar la solicitud de distancia
    resultado = gmaps.distance_matrix(
        origins=[f"{origen}, México"], 
        destinations=[f"{destino}, México"], 
        mode="driving", 
        departure_time=datetime.now()
        )
    
    elemento = resultado["rows"][0]["elements"][0]
    if elemento["status"] != "OK":
        raise ValueError("No se pudo calcular la distancia")
    
    distancia = elemento["distance"]["text"]
    duracion = elemento["duration"]["text"]
    return distancia, duracion