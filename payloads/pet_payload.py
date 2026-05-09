from faker import Faker
from models.pet_model import PetModel


class PetPayload:
    @staticmethod
    def get_one(exclude_keys: tuple = ()) -> dict:
        fake = Faker()

        initital_payload = {
            "id": fake.random_int(),
            "category": {
                "id": fake.random_int(1, 99),
                "name": fake.word()
            },
            "name": fake.first_name(),
            "photoUrls": [
                fake.url(), fake.url(), fake.url()
            ],
            "tags": [
                {
                    "id": fake.random_int(1, 99),
                    "name": fake.word()
                }
            ],
            "status": fake.enum(PetModel.Status)
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
            list_of_payloads.append(PetPayload.get_one(exclude_keys))

        return list_of_payloads
