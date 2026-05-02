import json
from config import *
from pydantic import ValidationError


class Validator:
    @staticmethod
    def validate(model_class, payload_or_response: dict) -> tuple:
        errors = []
        text_json = json.dumps(payload_or_response, indent=4, ensure_ascii=False)
        checked_keys = []

        try:
            model_class(**payload_or_response)
        except ValidationError as e:
            for i, error in enumerate(e.errors()):
                loc = tuple(error['loc'])
                msg = f"{error['msg']} ({error['type']})"
                pydantic_error = f"Ошибка валидации Pydantic #{i + 1}:\n* Суть ошибки: {msg}\n* Она связана с полем: {loc}"

                for key in payload_or_response.keys():
                    if loc[0] == key and key not in checked_keys:
                        text_json = text_json.replace(f'"{key}"', f'---> "{key}"')
                        checked_keys.append(key)

                if pydantic_error:
                    errors.append(pydantic_error)

        return (errors, text_json)

    @staticmethod
    def attach_files(errors: tuple, object_name: str = "") -> None:
        on = object_name
        if len(errors[0]) > 0:
            allure.attach("\n\n".join(errors[0]), attachment_type=TEXT, name=f"{on}Список ошибок ({len(errors[0])})")
            allure.attach(errors[1], attachment_type=TEXT, name=f"{on}Указания на ошибки")
