import requests
from tenacity import retry, stop_after_attempt, wait_random

class Micro1Service:
    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
    def get_data(self) -> None:
        headers = {'x-proffdock-attack': '{"actions":[{"name":"delay", "value":"10"}]}'}
        r = requests.get('http://localhost:5001/api/v1', headers=headers)
        if r.status_code == 200:
            print(r.json())
        else:
            raise BaseException("Error en el servicio 3")
