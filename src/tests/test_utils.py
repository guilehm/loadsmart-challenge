from src.utils import haversine


class TestHaversine:
    def test_method_should_accept_strings(self):
        haversine('37.5482697', '-121.9885719', '39.6001132', '-75.94133269999999')

    def test_method_should_accept_floats(self):
        haversine(37.5482697, -121.9885719, 39.6001132, -75.94133269999999)

    def test_method_should_accept_integers(self):
        haversine(37, -121, 39, -75)

    def test_should_return_expected_result(self):
        # compared with https://www.movable-type.co.uk/scripts/latlong.html
        # since this website rounds the number, i'm also doing so
        result_one = haversine(20, 30, 40, 50)
        result_two = haversine(29.5521737, -98.269734, 32.58847350000001, -95.20411349999999)
        assert round(result_one, 0) == 2927
        assert round(result_two, 1) == 446.3
