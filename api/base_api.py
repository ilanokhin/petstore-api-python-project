import json
from requests import Response
from api_client import ApiClient
from config import *
from validator import Validator


class BaseApi:
    def __init__(self):
        self.client = ApiClient()

    @staticmethod
    def standard_response_validation(response: Response, expected_status_code: int, model_class) -> None:
        with allure.step("Валидация ответа"):
            pretty_json = json.dumps(response.json(), indent=4, ensure_ascii=False)
            allure.attach(str(response.status_code), attachment_type=TEXT, name="Статус код")
            allure.attach(pretty_json, attachment_type=TEXT, name="Ответ")

            if expected_status_code < 400:
                errors = Validator.validate(model_class, response.json())
                Validator.attach_files(errors)
                assert not errors[0], f"{errors[0][0]}\n\nДополнительная информация в приложенных файлах"

            assert response.status_code == expected_status_code, f"Статус код: {response.status_code}"

    @staticmethod
    def list_response_validation(response: Response, expected_status_code: int, model_class, unit_name: str,
                                 unit_key: str, symbol: str = "#") -> None:
        with allure.step("Валидация ответа"):
            pretty_json = json.dumps(response.json(), indent=4, ensure_ascii=False)
            allure.attach(str(response.status_code), attachment_type=TEXT, name="Статус код")
            allure.attach(pretty_json, attachment_type=TEXT, name=f"Ответ ({len(response.json())})")

            if expected_status_code < 400:
                first_error = ""

                for unit_data in response.json():
                    errors = Validator.validate(model_class, unit_data)
                    unit = f"[{unit_name} {symbol}{unit_data[unit_key]}] "
                    Validator.attach_files(errors, unit)

                    if not first_error and errors[0]:
                        first_error = f"{unit}\n{errors[0][0]}"

                assert not first_error, f"{first_error}\n\nДополнительная информация в приложенных файлах"

            assert response.status_code == expected_status_code, f"Статус код: {response.status_code}"

    @staticmethod
    def list_payload_validation(payload: list[dict], model_class, unit_name: str, unit_key: str,
                                symbol: str = "#") -> None:
        with allure.step("Валидация запроса"):
            pretty_json = json.dumps(payload, indent=4, ensure_ascii=False)
            allure.attach(pretty_json, attachment_type=TEXT, name="Тело запроса")

            first_error = ""
            for unit_data in payload:
                errors = Validator.validate(model_class, unit_data)
                unit = f"[{unit_name} {symbol}{unit_data[unit_key]}] "
                Validator.attach_files(errors, unit)

                if not first_error and errors[0]:
                    first_error = f"{unit}\n{errors[0][0]}"

            assert not first_error, f"{first_error}\n\nДополнительная информация в приложенных файлах"

    @staticmethod
    def standard_payload_validation(payload: dict, model_class) -> None:
        with allure.step("Валидация запроса"):
            pretty_json = json.dumps(payload, indent=4, ensure_ascii=False)
            allure.attach(pretty_json, attachment_type=TEXT, name="Тело запроса")
            errors = Validator.validate(model_class, payload)
            Validator.attach_files(errors)
            assert not errors[0], f"{errors[0][0]}\n\nДополнительная информация в приложенных файлах"
