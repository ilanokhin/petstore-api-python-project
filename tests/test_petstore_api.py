import pytest
import allure
from payloads.pet_payload import PetPayload
from payloads.order_payload import OrderPayload
from payloads.user_payload import UserPayload
from models.pet_model import PetModel


@allure.suite("Тестирование Petstore API")
class TestPetstoreApi():
    @pytest.mark.xfail
    @pytest.mark.pet_group
    @allure.title("Полный цикл работы с питомцем")
    def test_pet_group(self, pet, fake):
        payload = PetPayload.get_one(exclude_keys=("category", "tags"))

        pet.add_new_pet(payload)
        pet.upload_pet_image(pet_id=payload["id"], file_path="data/images/dog1.jpg")

        with allure.step("Получить данные питомца по ID, проверить, что они совпадают с ранее отправленными"):
            response = pet.get_pet_by_id(pet_id=payload["id"]).json()
            check = True

            for key in payload.keys():
                if payload[key] != response[key]:
                    check = False
                    break

            assert check, "Полученные данные не совпадают с отправленными"

        with allure.step("Обновить статус питомца"):
            new_status = fake.enum(PetModel.Status)
            while payload["status"] == new_status:
                new_status = fake.enum(PetModel.Status)

            payload["status"] = new_status
            pet.update_pet(payload)

        with allure.step("Обновить имя питомца через форму"):
            payload["name"] = fake.first_name()
            pet.update_pet_with_form(pet_id=payload["id"], name=payload["name"])

        with allure.step("Получить имя и статус питомца по ID, проверить, что они обновились"):
            response = pet.get_pet_by_id(pet_id=payload["id"]).json()
            assert payload["name"] == response["name"], "Имя питомца не обновлено"
            assert payload["status"] == response["status"], "Статус питомца не обновлён"

        pet.delete_pet(pet_id=payload["id"])
        pet.get_pet_by_id(pet_id=payload["id"], expected_status_code=404)
        pet.find_pets_by_status(status=fake.enum(PetModel.Status))

    @pytest.mark.store_group
    @allure.title("Управление заказами и инвентарём")
    def test_store_group(self, store, fake):
        payload = OrderPayload.get_one(exclude_keys=("shipDate",))

        with allure.step("Получить инвентарь, проверить, что он содержит статусы 'available', 'pending' и 'sold'"):
            response = store.get_inventory().json()
            assert 'available' in response.keys(), "Инвентарь не содержит статус 'available'"
            assert 'pending' in response.keys(), "Инвентарь не содержит статус 'pending'"
            assert 'sold' in response.keys(), "Инвентарь не содержит статус 'sold'"

        store.place_order(payload)

        with allure.step("Получить данные заказа по ID, проверить, что они совпадают с ранее отправленными"):
            response = store.get_order_by_id(order_id=payload["id"]).json()
            check = True

            for key in payload.keys():
                if payload[key] != response[key]:
                    check = False
                    break

            assert check, "Полученные данные не совпадают с отправленными"

        store.delete_order(order_id=payload["id"])
        store.get_order_by_id(order_id=payload["id"], expected_status_code=404)

    @pytest.mark.user_group
    @allure.title("Полный цикл управления пользователями")
    def test_user_group(self, user, fake):
        payload = UserPayload.get_one()
        payload_list = UserPayload.get_list(5)

        user.create_users_with_list(payload_list)

        with allure.step("Получить второго пользователя по username, проверить, что данные соответствуют отправленным"):
            response = user.get_user_by_username(username=payload_list[1]["username"]).json()
            check = True

            for key in payload_list[1].keys():
                if payload_list[1][key] != response[key]:
                    check = False
                    break

            assert check, "Полученные данные не соответствуют отправленным"

        user.create_user(payload)

        with allure.step("Получить пользователя по username, проверить, что данные соответствуют отправленным"):
            response = user.get_user_by_username(username=payload["username"]).json()
            check = True

            for key in payload.keys():
                if payload[key] != response[key]:
                    check = False
                    break

            assert check, "Полученные данные не соответствуют отправленным"

        with allure.step("Обновить телефон и email пользователя"):
            payload["phone"] = fake.basic_phone_number()
            payload["email"] = fake.email()
            user.update_user(username=payload["username"], payload=payload)

        with allure.step("Получить телефон и email пользователя по username, проверить, что они обновлены"):
            response = user.get_user_by_username(username=payload["username"]).json()
            assert payload["phone"] == response["phone"], "Телефон пользователя не обновлён"
            assert payload["email"] == response["email"], "Email пользователя не обновлён"

        user.login_user(username=payload["username"], password=payload["password"])
        user.logout_user()
        user.delete_user(username=payload["username"])
        user.get_user_by_username(username=payload["username"], expected_status_code=404)
