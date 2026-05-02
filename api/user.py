from requests import Response
from api.base_api import BaseApi
from config import *
from models.user_model import UserModel
from models.api_response_model import ApiResponseModel


class User(BaseApi):
    @allure.step("Создание пользователя: POST /user")
    def create_user(self, payload: dict, expected_status_code: int = 200) -> Response:
        super().standard_payload_validation(payload, UserModel)
        response = self.client.post("/user", json=payload, headers=API_HEADERS)
        super().standard_response_validation(response, expected_status_code, ApiResponseModel)
        return response

    @allure.step("Создание пользователей из списка: POST /user/createWithList")
    def create_users_with_list(self, payload_list: list[dict], expected_status_code: int = 200) -> Response:
        super().list_payload_validation(payload_list, UserModel, "Пользователь", "username", "@")
        response = self.client.post("/user/createWithList", json=payload_list, headers=API_HEADERS)
        super().standard_response_validation(response, expected_status_code, ApiResponseModel)
        return response

    @allure.step("Вход пользователя: GET /user/login")
    def login_user(self, username: str, password: str, expected_status_code: int = 200) -> Response:
        params = dict(username=username, password=password)
        response = self.client.get("/user/login", params=params)
        super().standard_response_validation(response, expected_status_code, ApiResponseModel)
        return response

    @allure.step("Выход пользователя: GET /user/logout")
    def logout_user(self, expected_status_code: int = 200) -> Response:
        response = self.client.get("/user/logout")
        super().standard_response_validation(response, expected_status_code, ApiResponseModel)
        return response

    @allure.step("Получение пользователя по username: GET /user/{{username}}")
    def get_user_by_username(self, username: str, expected_status_code: int = 200) -> Response:
        response = self.client.get(f"/user/{username}")
        super().standard_response_validation(response, expected_status_code, UserModel)
        return response

    @allure.step("Обновление пользователя: PUT /user/{{username}}")
    def update_user(self, username: str, payload: dict, expected_status_code: int = 200) -> Response:
        body = {}
        for key, value in payload.items():
            body[key] = value

        super().standard_payload_validation(body, UserModel)
        response = self.client.put(f"/user/{username}", json=body, headers=API_HEADERS)
        super().standard_response_validation(response, expected_status_code, ApiResponseModel)
        return response

    @allure.step("Удаление пользователя: DELETE /user/{{username}}")
    def delete_user(self, username: str, expected_status_code: int = 200) -> Response:
        response = self.client.delete(f"/user/{username}")
        super().standard_response_validation(response, expected_status_code, ApiResponseModel)
        return response
