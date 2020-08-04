from collections import Counter

from src.utils import get_csv_reader, haversine


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
        return f'COMBINATION: C#{self.cargo.id:02} - T#{self.truck.id:03} - D {self.distance_to_load_representation} km'


class TrucksAndCargo:
    def __init__(self):
        self.trucks = self._get_model_list('trucks')
        self.cargos = self._get_model_list('cargo')
        self.combinations = self._create_combinations()

        self.closer_combinations = list(self._get_closer_combinations())

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


trucks_and_cargos = TrucksAndCargo()
for i in trucks_and_cargos.combinations:
    print(i)

