import requests    #реалізує функціональність для роботи з REST API іншого користувача.
                   # Він використовує бібліотеку requests для відправлення HTTP-запитів до сервера

class NetworkHelper:
    BASE_URL = 'http://127.0.0.1:8000/api/'
    # додати Admin - password
    @staticmethod
    def get_list():
        """Метод для отримання списку об'єктів."""
        try:
            response = requests.get(f"{NetworkHelper.BASE_URL}objects/")
            response.raise_for_status()  # перевірка статусу відповіді
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during GET list request: {e}")
            return None

    @staticmethod
    def get_item(item_id):
        """Метод для отримання конкретного об'єкта за його ID."""
        try:
            response = requests.get(f"{NetworkHelper.BASE_URL}objects/{item_id}/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during GET item request: {e}")
            return None

    def delete_item(self, item_id):
        url = f"{self.API_URL}{item_id}/"
        response = requests.delete(url)
        if response.status_code == 204:  # 204 означає успішне видалення
            return True
        else:
            print("Помилка видалення об’єкта:", response.status_code, response.text)
            return False


