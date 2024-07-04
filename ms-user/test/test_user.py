# test_retry.py

import requests
from retrying import retry
import time

# Definición de la función que utiliza retry
@retry(stop_max_attempt_number=3, wait_fixed=1000, retry_on_exception=lambda e: isinstance(e, (requests.exceptions.Timeout, requests.exceptions.ConnectionError)))
def get_cabins():
    # Intenta hacer una solicitud HTTP
    print("Haciendo solicitud...")
    response = requests.get('https://user.eden.localhost/api/v1/cabins')
    response.raise_for_status()
    return response.json()

# Función para ejecutar la prueba
def run_test():
    try:
        cabins = get_cabins()
        print("Cabins obtenidos correctamente:", cabins)
    except Exception as e:
        print("Error al obtener cabins:", e)

# Ejecutar la prueba
if __name__ == "__main__":
    run_test()
