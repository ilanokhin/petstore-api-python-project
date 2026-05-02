import os
import allure

API_BASE_URL = os.getenv("API_BASE_URL", "https://petstore.swagger.io/v2")
API_HEADERS = {"Content-Type": "application/json"}

TEXT = allure.attachment_type.TEXT