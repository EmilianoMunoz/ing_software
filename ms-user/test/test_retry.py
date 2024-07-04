import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.services.user import UserService

class TestUserService(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)  # Crear una aplicación Flask para las pruebas
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.services.user.requests.get')  # Ajusta la ruta según la estructura de tu proyecto
    def test_get_cabins_retry(self, mock_get):
        # Configuramos el mock para simular un fallo de conexión en el primer intento
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = [ConnectionError, None]  # Simulamos ConnectionError en el primer intento
        mock_response.status_code = 500
        mock_response.json.return_value = {'error': 'Connection error'}
        mock_get.return_value = mock_response
        
        # Creamos una instancia del servicio UserService
        service = UserService()
        
        # Ejecutamos el método que debería aplicar retry
        try:
            service.get_cabins()
        except Exception as e:
            # Verificamos que se haya intentado el número correcto de veces (2 intentos en total debido a retry)
            self.assertEqual(mock_get.call_count, 2)
            self.assertEqual(str(e), "An error occurred while trying to communicate with the cabin service")

if __name__ == '__main__':
    unittest.main()

