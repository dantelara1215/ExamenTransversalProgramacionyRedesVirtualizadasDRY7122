import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "c94633a6-fd37-4d91-9b7a-9dfc372c2f46"

def geocoding(location, key):
    while location == "":
        location = input("Ingrese la ubicación nuevamente: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_status = replydata.status_code
    json_data = replydata.json()

    if json_status == 200 and len(json_data["hits"]) != 0:
        json_data = requests.get(url).json()
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        country = json_data["hits"][0]["country"] if "country" in json_data["hits"][0] else ""
        state = json_data["hits"][0]["state"] if "state" in json_data["hits"][0] else ""

        if state and country:
            new_loc = name + ", " + state + ", " + country
        elif state:
            new_loc = name + ", " + country
        else:
            new_loc = name

        print("URL de la API de geocodificación para " + new_loc + " (Tipo de ubicación: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de la API de geocodificación: " + str(json_status) + "\nMensaje de error: " + json_data["message"])
    return json_status, lat, lng, new_loc

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículo disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile = ["car", "bike", "foot"]
    vehicle = input("Ingrese un perfil de vehículo de la lista anterior (o 's' para salir): ")

    if vehicle.lower() == "salir" or vehicle.lower() == "s":  # Salir si se ingresa "s" o "salir"
        break
    elif vehicle in profile:
        vehicle = vehicle
    else:
        vehicle = "car"
        print("No se ingresó un perfil de vehículo válido. Usando el perfil de coche.")

    loc1 = input("Ciudad de Origen: ")
    if loc1.lower() == "salir" or loc1.lower() == "s":  # Salir si se ingresa "s" o "salir"
        break
    orig = geocoding(loc1, key)
    loc2 = input("Ciudad de Destino: ")
    if loc2.lower() == "salir" or loc2.lower() == "s":  # Salir si se ingresa "s" o "salir"
        break
    dest = geocoding(loc2, key)
    print("=================================================")

    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle, "locale": "es"}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()

        print("Estado de la API de rutas: " + str(paths_status) + "\nURL de la API de rutas:\n" + paths_url)
        print("=================================================")
        print("Direcciones desde " + orig[3] + " hasta " + dest[3] + " en " + vehicle)
        print("=================================================")

        if paths_status == 200:
            km = round(paths_data["paths"][0]["distance"] / 1000, 2)
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print("Distancia recorrida: {:.2f} km".format(km))
            print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")

            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = round(paths_data["paths"][0]["instructions"][each]["distance"] / 1000, 2)
                print("{0} ({1:.2f} km)".format(path, distance))
            print("=============================================")

        else:
            print("Mensaje de error: " + paths_data["message"])
            print("*****************")