import itertools
from collections import Counter
from itertools import combinations_with_replacement

from src.utils import get_csv_reader, haversine

PRECISION = 100


class Cargo:
    def __init__(self, _id, kwargs):
        self.id = _id
        self.product = kwargs.pop('product')
        self.origin_city = kwargs.pop('origin_city')
        self.origin_state = kwargs.pop('origin_state')
        self.origin_lat = kwargs.pop('origin_lat')
        self.origin_lng = kwargs.pop('origin_lng')
        self.destination_city = kwargs.pop('destination_city')
        self.destination_state = kwargs.pop('destination_state')
        self.destination_lat = kwargs.pop('destination_lat')
        self.destination_lng = kwargs.pop('destination_lng')

    def __repr__(self):
        return f'Cargo #{self.id} - [{self.origin_state}-{self.destination_state}] - {self.product}'


class Truck:
    def __init__(self, _id, kwargs):
        self.id = _id
        self.available = True
        self.truck = kwargs.pop('truck')
        self.city = kwargs.pop('city')
        self.state = kwargs.pop('state')
        self.lat = kwargs.pop('lat')
        self.lng = kwargs.pop('lng')

    def __repr__(self):
        return f'Truck #{self.id} - {self.truck}'


class Combination:
    def __init__(self, truck, cargo):
        self.id = None
        self.truck = truck
        self.cargo = cargo

    @property
    def distance_to_load(self):
        return haversine(
            origin_lat=self.truck.lat,
            origin_lng=self.truck.lng,
            destination_lat=self.cargo.origin_lat,
            destination_lng=self.cargo.origin_lng,
        )

    @property
    def distance_to_load_representation(self):
        return f'{round(self.distance_to_load, 2):7}'

    def __lt__(self, other):
        return self.distance_to_load < other.distance_to_load

    def __le__(self, other):
        return self.distance_to_load <= other.distance_to_load

    def __gt__(self, other):
        return self.distance_to_load > other.distance_to_load

    def __ge__(self, other):
        return self.distance_to_load >= other.distance_to_load

    def __eq__(self, other):
        return self.distance_to_load == other.distance_to_load

    def __repr__(self):
        return f'COMBINATION: C#{self.cargo.id:02} - T#{self.truck.id:03} - D {self.distance_to_load_representation} km - ID {self.id}'


class TrucksAndCargo:
    def __init__(self):
        self.trucks = self._get_model_list('trucks')
        self.cargos = self._get_model_list('cargo')
        self.combinations = self._create_combinations()

        self.closer_combinations = list(self._get_closer_combinations())
        self.filtered_combinations = list()
        self.valid_combinations_ids = list()
        self._fill_combination_ids()

    @staticmethod
    def _get_model_list(model):
        if model not in 'cargo trucks'.split():
            raise NameError(f'The model {model} is not valid.')
        Model = Cargo if model == 'cargo' else Truck
        return [Model(_id, data) for _id, data in enumerate(get_csv_reader(model), 1)]

    def _create_combinations(self):
        return [Combination(truck, cargo) for cargo in self.cargos for truck in self.trucks]

    def closer_trucks(self, cargo_id):
        combinations = filter(lambda x: x.cargo.id == cargo_id, self.combinations)
        return sorted(combinations, key=lambda x: x.distance_to_load)

    def _get_closer_combinations(self):
        for cargo in self.cargos:
            yield self.closer_trucks(cargo.id)

    def filter_closer_combinations(self):
        for combination in self.closer_combinations:
            self.filtered_combinations.append(
                list(filter(lambda x: x.distance_to_load < combination[0].distance_to_load + PRECISION, combination))
            )

    # TODO: Choose a better name
    def get_conflict_combinations(self, position=0):
        trucks_ids = (combination[0].truck.id for combination in self.closer_combinations)
        repeated_trucks_ids = [truck for truck, count in Counter(trucks_ids).items() if count > 1]
        conflict_combinations = [filter(
            lambda x: x[position].truck.id == _id, self.closer_combinations
        ) for _id in repeated_trucks_ids]
        return conflict_combinations

    def print_total_distance(self):
        print(sum(combination[0].distance_to_load for combination in self.closer_combinations))

    @staticmethod
    def get_distance_ids():
        # TODO: count the numbers from the sheet
        letters = range(1, 8)
        numbers = range(1, 45)
        distances_ids = [f'{letter},{number}' for letter in letters for number in numbers]
        return distances_ids

    def _fill_combination_ids(self):
        for number, _id in enumerate(self.get_distance_ids()):
            self.combinations[number].id = _id

    def zip_combinations_with_ids(self):
        return zip(self.combinations, self.get_distance_ids())

    def get_filtered_ids(self):
        return [comb.id for comb in itertools.chain.from_iterable(self.filtered_combinations)]

    def create_generator(self):
        generator = combinations_with_replacement(self.get_filtered_ids(), 7)
        valid_combinations = list()
        for combination in generator:
            cargos = list()
            trucks = list()
            for cargo, truck in [comb.split(',') for comb in combination]:
                cargos.append(cargo)
                trucks.append(truck)
            if len(set(cargos)) == 7 and len(set(trucks)) == 7:
                valid_combinations.append(combination)
        self.valid_combinations_ids = valid_combinations
        return valid_combinations

    def sum_distance_from_valid_combinations_ids(self):
        distances = list()
        for ids in self.valid_combinations_ids:
            combinations = filter(lambda x: x.id in ids, self.combinations)
            total = sum([x.distance_to_load for x in combinations])
            distances.append(total)
        key, _ = min(enumerate(distances), key=lambda x: x[1])
        best_combination = self.valid_combinations_ids[key]
        return best_combination
