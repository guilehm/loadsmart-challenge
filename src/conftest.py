import pytest

from src.models import Cargo, Combination, Truck


@pytest.fixture
def truck_1():
    return Truck(_id=1, lat='35', lng='-87')


@pytest.fixture
def truck_2():
    return Truck(_id=2, lat='40', lng='-87')


@pytest.fixture
def cargo_1():
    return Cargo(_id=1, origin_lat='41', origin_lng='-87')


@pytest.fixture
def cargo_2():
    return Cargo(_id=2, origin_lat='41.5', origin_lng='-87.5')


@pytest.fixture
def combination_1(truck_1, cargo_1):
    return Combination(truck=truck_1, cargo=cargo_1)


@pytest.fixture
def combination_2(truck_2, cargo_2):
    return Combination(truck=truck_2, cargo=cargo_2)
