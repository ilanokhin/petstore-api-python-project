from requests import Response
from api.base_api import BaseApi
from config import *
from models.order_model import OrderModel
from models.api_response_model import ApiResponseModel


class Store(BaseApi):
    @allure.step("Получение инвентаря: GET /store/inventory")
    def get_inventory(self, expected_status_code: int = 200) -> Response:
        response = self.client.get("/store/inventory")
        super().standard_response_validation(response, expected_status_code, None)
        return response

    @allure.step("Создание заказа: POST /store/order")
    def place_order(self, payload: dict, expected_status_code: int = 200) -> Response:
        super().standard_payload_validation(payload, OrderModel)
        response = self.client.post("/store/order", json=payload, headers=API_HEADERS)
        super().standard_response_validation(response, expected_status_code, OrderModel)
        return response

    @allure.step("Получение заказа по ID: GET /store/order/{{orderId}}")
    def get_order_by_id(self, order_id: int, expected_status_code: int = 200) -> Response:
        response = self.client.get(f"/store/order/{order_id}")
        super().standard_response_validation(response, expected_status_code, OrderModel)
        return response

    @allure.step("Удаление заказа: DELETE /store/order/{{orderId}}")
    def delete_order(self, order_id: int, expected_status_code: int = 200) -> Response:
        response = self.client.delete(f"/store/order/{order_id}")
        super().standard_response_validation(response, expected_status_code, ApiResponseModel)
        return response
