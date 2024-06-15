import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Desactivar advertencias por no verificar el certificado SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Definimos la URL del endpoint que queremos probar
url = "https://user.eden.localhost/api/v1/all_cabins"

try:
    # Realizamos la solicitud GET, desactivando la verificación del certificado SSL
    response = requests.get(url, verify=False)

    # Verificamos si la solicitud fue exitosa (código 200)
    if response.status_code == 200:
        print("Test exitoso. Se pudo obtener la lista de cabañas correctamente.")
        print("Respuesta del servidor:")
        print(response.json())  # Mostramos la respuesta del servidor
    else:
        print(f"Error: La solicitud no fue exitosa. Código de estado: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error al realizar la solicitud: {e}")
