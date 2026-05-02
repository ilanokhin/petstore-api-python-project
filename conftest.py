import pytest
from faker import Faker
from api.pet import Pet
from api.store import Store
from api.user import User


@pytest.fixture
def fake():
    return Faker()

@pytest.fixture
def pet():
    return Pet()

@pytest.fixture
def store():
    return Store()

@pytest.fixture
def user():
    return User()