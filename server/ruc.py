import requests

def validar_ruc(ruc):
    url = "https://srienlinea.sri.gob.ec/sri-catastro-sujeto-servicio-internet/rest/ConsolidadoContribuyente/existePorNumeroRuc"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    params = {
        "numeroRuc": ruc  # Cambié el nombre del parámetro aquí
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            resultado = response.json()
            if resultado is True:
                print(f"El RUC {ruc} SÍ existe.")
                return True
            else:
                print(f"El RUC {ruc} NO existe.")
                return False
        else:
            print(f"Error HTTP: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return None

# Prueba
validar_ruc("1710631670001")
