import googlemaps
from datetime import datetime

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

"""
if __name__ == "__main__":
    origen = "Cancun"
    destino = "Tijuana"

    

"""