import requests
from retrying import retry

url = 'https://user.eden.localhost/api/v1/cabins'


@retry(stop_max_attempt_number=3, wait_fixed=1000, retry_on_result=lambda result: result is None)
def get_cabins():
    print("Intentando obtener cabins...")
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        print(f"Respuesta no exitosa: {response.status_code}")
        return None
    return response.json()

def run_test():
    try:
        cabins = get_cabins()
        if cabins is not None:
            print("Cabins obtenidos correctamente:", cabins)
        else:
            print("No se pudieron obtener cabins después de varios intentos.")
    except Exception as e:
        print("Error al obtener cabins:", e)

if __name__ == "__main__":
    run_test()