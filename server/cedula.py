import requests

def validar_cedula(cedula):
    url = "https://srienlinea.sri.gob.ec/sri-registro-civil-servicio-internet/rest/DatosRegistroCivil/existeNumeroIdentificacion"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    params = {
        "numeroIdentificacion": cedula
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            resultado = response.json()
            if resultado is True:
                print(f"La cédula {cedula} SÍ existe.")
                return True
            else:
                print(f"La cédula {cedula} NO existe.")
                return False
        else:
            print(f"Error HTTP: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return None

# Prueba
validar_cedula("17285734842r")
