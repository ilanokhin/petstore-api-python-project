from faker import Faker
from models.order_model import OrderModel


class OrderPayload:
    @staticmethod
    def get_one(exclude_keys: tuple = ()) -> dict:
        fake = Faker()
        initital_payload = {
            "id": fake.random_int(),
            "petId": fake.random_int(),
            "quantity": 1,
            "shipDate": str(fake.date_this_year()),
            "status": fake.enum(OrderModel.Status),
            "complete": fake.boolean()
        }

        final_payload = {}
        for key in initital_payload:
            if key not in exclude_keys:
                final_payload[key] = initital_payload[key]

        return final_payload

    @staticmethod
    def get_list(number: int = 3, exclude_keys: tuple = ()) -> list[dict]:
        list_of_payloads = []
        for i in range(number):
            list_of_payloads.append(OrderPayload.get_one(exclude_keys))

        return list_of_payloads
