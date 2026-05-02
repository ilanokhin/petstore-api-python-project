from faker import Faker


class UserPayload:
    @staticmethod
    def get_one(exclude_keys: tuple = ()) -> dict:
        fake = Faker()
        initital_payload = {
            "id": fake.random_int(),
            "username": fake.user_name(),
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "email": fake.email(),
            "password": fake.password(),
            "phone": fake.basic_phone_number(),
            "userStatus": fake.random_int(0, 1)
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
            list_of_payloads.append(UserPayload.get_one(exclude_keys))

        return list_of_payloads
