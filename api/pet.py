from requests import Response
from api.base_api import BaseApi
from config import *
from models.pet_model import PetModel
from models.api_response_model import ApiResponseModel


class Pet(BaseApi):
    @allure.step("Загрузка изображения питомца: POST /pet/{{petId}}/uploadImage")
    def upload_pet_image(self, pet_id: int, file_path: str, additional_metadata: str = None,
                         expected_status_code: int = 200) -> Response:
        files = {"file": open(file_path, "rb")}
        data = {}
        if additional_metadata is not None:
            data["additionalMetadata"] = additional_metadata

        response = self.client.post(f"/pet/{pet_id}/uploadImage", files=files, data=data)
        super().standard_response_validation(response, expected_status_code, ApiResponseModel)
        return response

    @allure.step("Добавление нового питомца: POST /pet")
    def add_new_pet(self, payload: dict, expected_status_code: int = 200) -> Response:
        super().standard_payload_validation(payload, PetModel)
        response = self.client.post("/pet", json=payload, headers=API_HEADERS)
        super().standard_response_validation(response, expected_status_code, PetModel)
        return response

    @allure.step("Обновление существующего питомца: PUT /pet")
    def update_pet(self, payload: dict, expected_status_code: int = 200) -> Response:
        super().standard_payload_validation(payload, PetModel)
        response = self.client.put("/pet", json=payload, headers=API_HEADERS)
        super().standard_response_validation(response, expected_status_code, PetModel)
        return response

    @allure.step("Поиск питомцев по статусу: GET /pet/findByStatus")
    def find_pets_by_status(self, status: list, expected_status_code: int = 200) -> Response:
        params = dict(status=status)
        response = self.client.get("/pet/findByStatus", params=params)
        super().list_response_validation(response, expected_status_code, PetModel, "Питомец", "id")
        return response

    @allure.step("Получение питомца по ID: GET /pet/{{petId}}")
    def get_pet_by_id(self, pet_id: int, expected_status_code: int = 200) -> Response:
        response = self.client.get(f"/pet/{pet_id}")
        super().standard_response_validation(response, expected_status_code, PetModel)
        return response

    @allure.step("Обновление питомца через форму: POST /pet/{{petId}}")
    def update_pet_with_form(self, pet_id: int, name: str = None, status: str = None,
                             expected_status_code: int = 200) -> Response:
        data = {}
        if name is not None:
            data["name"] = name
        if status is not None:
            data["status"] = status

        response = self.client.post(f"/pet/{pet_id}", data=data)
        super().standard_response_validation(response, expected_status_code, ApiResponseModel)
        return response

    @allure.step("Удаление питомца: DELETE /pet/{{petId}}")
    def delete_pet(self, pet_id: int, expected_status_code: int = 200) -> Response:
        response = self.client.delete(f"/pet/{pet_id}")
        super().standard_response_validation(response, expected_status_code, ApiResponseModel)
        return response
