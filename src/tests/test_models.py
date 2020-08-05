from src.models import TrucksAndCargos, CombinationCombo, Truck, Cargo
from src.utils import haversine


class TestTruckAndCargos:

    @staticmethod
    def get_result():
        trucks_and_cargos = TrucksAndCargos()
        return trucks_and_cargos.best_combo

    def test_should_return_combinations_for_all_cargos(self):
        trucks_and_cargos = TrucksAndCargos()
        result = trucks_and_cargos.best_combo
        assert len(result) == trucks_and_cargos.CARGO_COUNT

    def test_should_return_a_combination_combo_instance(self):
        result = self.get_result()
        assert isinstance(result, CombinationCombo)

    def test_should_not_return_repeated_trucks(self):
        result = self.get_result()
        trucks_ids = [combination.truck.id for combination in result.combinations]
        assert len(trucks_ids) == len(set(trucks_ids))

    def test_best_combo_should_be_the_one_with_minimum_total_distance(self):
        trucks_and_cargos = TrucksAndCargos()
        chosen_combo = trucks_and_cargos.best_combo
        all_combos = trucks_and_cargos.combos
        best_combo = min(all_combos, key=lambda x: x.total_distance)
        assert chosen_combo is best_combo

    def test_should_untie_correctly(self, truck_1, truck_2, cargo_1, cargo_2):
        # truck 1 is closer to both cargos
        # cargo_1 to truck_1 = 111km
        # cargo_1 to truck_2 = 667km
        # cargo_2 to truck_1 = 172km
        # cargo_2 to truck_2 = 724km
        # is better to truck_2 get cargo_1 because 111km is closer than 172km
        # and the difference between 724km and 667km does not compensate it

        trucks_and_cargos = TrucksAndCargos(trucks=[truck_1, truck_2], cargos=[cargo_1, cargo_2])
        combination_a, combination_b = trucks_and_cargos.best_combo
        assert combination_a.truck == truck_2
        assert combination_a.cargo == cargo_1
        assert combination_b.truck == truck_1
        assert combination_b.cargo == cargo_2


class TestCombination:

    def test_combination_should_calculate_correct_distance_to_load(self, combination_1):
        truck = combination_1.truck
        cargo = combination_1.cargo
        distance_to_load = haversine(
            origin_lat=truck.lat,
            origin_lng=truck.lng,
            destination_lat=cargo.origin_lat,
            destination_lng=cargo.origin_lng,
        )
        assert combination_1.distance_to_load == distance_to_load

    def test_comparing_combinations_should_work(self, combination_1, combination_2):
        assert combination_1.distance_to_load == 667.1695598673526
        assert combination_2.distance_to_load == 172.0271888537456
        assert combination_1 > combination_2
        assert combination_1 >= combination_2
        assert combination_2 < combination_1
        assert combination_2 <= combination_1
        assert combination_1 == combination_1
