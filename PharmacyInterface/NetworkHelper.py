import requests
from requests.auth import HTTPBasicAuth

class NetworkHelper:
    BASE_URL = 'http://127.0.0.1:8000/api/'  # Замініть на адресу вашого API
    USERNAME = 'n'  # Замініть на ваше ім'я користувача
    PASSWORD = 'zalupa'  # Замініть на ваш пароль

    @staticmethod
    def get_list(endpoint):
        """Метод для отримання списку об'єктів."""
        try:
            response = requests.get(
                f"{NetworkHelper.BASE_URL}{endpoint}/",
                auth=HTTPBasicAuth(NetworkHelper.USERNAME, NetworkHelper.PASSWORD)
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during GET list request: {e}")
            return None

    @staticmethod
    def get_item(endpoint, item_id):
        """Метод для отримання конкретного об'єкта за його ID."""
        try:
            response = requests.get(
                f"{NetworkHelper.BASE_URL}{endpoint}/{item_id}/",
                auth=HTTPBasicAuth(NetworkHelper.USERNAME, NetworkHelper.PASSWORD)
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during GET item request: {e}")
            return None

    @staticmethod
    def create_item(endpoint, data):
        """Метод для створення нового об'єкта."""
        try:
            response = requests.post(
                f"{NetworkHelper.BASE_URL}{endpoint}/",
                json=data,
                auth=HTTPBasicAuth(NetworkHelper.USERNAME, NetworkHelper.PASSWORD)
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during POST request: {e}")
            return None

    @staticmethod
    def update_item(endpoint, item_id, data):
        """Метод для оновлення об'єкта за ID через API."""
        try:
            response = requests.put(
                f"{NetworkHelper.BASE_URL}{endpoint}/{item_id}/",
                json=data,
                auth=HTTPBasicAuth(NetworkHelper.USERNAME, NetworkHelper.PASSWORD)
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during PUT request: {e}")
            return None

    @staticmethod
    def delete_item(endpoint, item_id):
        """Метод для видалення об'єкта за ID."""
        try:
            response = requests.delete(
                f"{NetworkHelper.BASE_URL}{endpoint}/{item_id}/",
                auth=HTTPBasicAuth(NetworkHelper.USERNAME, NetworkHelper.PASSWORD)
            )
            response.raise_for_status()
            return {"status": "success"}
        except requests.exceptions.RequestException as e:
            print(f"Error during DELETE request: {e}")
            return None
