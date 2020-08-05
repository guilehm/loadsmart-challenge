from itertools import combinations_with_replacement, chain

from src.utils import get_csv_reader, haversine


class Cargo:
    def __init__(self, _id, **kwargs):
        self.id = _id
        self.product = kwargs.get('product')
        self.origin_city = kwargs.get('origin_city')
        self.origin_state = kwargs.get('origin_state')
        self.origin_lat = kwargs.pop('origin_lat')
        self.origin_lng = kwargs.pop('origin_lng')
        self.destination_city = kwargs.get('destination_city')
        self.destination_state = kwargs.get('destination_state')
        self.destination_lat = kwargs.get('destination_lat')
        self.destination_lng = kwargs.get('destination_lng')

    def __repr__(self):
        return f'Cargo #{self.id} - [{self.origin_state or ""}-{self.destination_state or ""}] - {self.product or ""}'


class Truck:
    def __init__(self, _id, **kwargs):
        self.id = _id
        self.truck = kwargs.get('truck')
        self.city = kwargs.get('city')
        self.state = kwargs.get('state')
        self.lat = kwargs.pop('lat')
        self.lng = kwargs.pop('lng')

    def __repr__(self):
        return f'Truck #{self.id} - {self.truck or ""}'


class Combination:
    def __init__(self, truck, cargo):
        self.cargo = cargo
        self.truck = truck
        self.id = f'{self.cargo.id},{self.truck.id}'

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
        return f'COMB#{self.id:4}: ' \
               f'(C#{self.cargo.id:03}-' \
               f'T#{self.truck.id:03}) ' \
               f'(D {self.distance_to_load_representation}km)'


class CombinationCombo:
    def __init__(self, *combinations):
        self.combinations = combinations

    @property
    def total_distance(self):
        return sum(c.distance_to_load for c in self.combinations)

    def __len__(self):
        return len(self.combinations)

    def __iter__(self):
        return (combination for combination in self.combinations)

    def __repr__(self):
        return f'COMB.COMBO: {self.total_distance:6.2f}km'

    def print_combinations(self):
        for combination in self.combinations:
            print(f'\t{combination}')


class TrucksAndCargos:
    THRESHOLD = 50

    def __init__(self, threshold=THRESHOLD, trucks=None, cargos=None):
        self.threshold = threshold
        self.trucks = trucks or self._get_model_list('trucks')
        self.cargos = cargos or self._get_model_list('cargo')
        self.combinations = self._create_combinations()
        self.closer_combinations = list(self._get_closer_combinations())

        self.combos = list()
        self._best_combo = None

        self.TRUCK_COUNT = len(self.trucks)
        self.CARGO_COUNT = len(self.cargos)

    @staticmethod
    def _get_model_list(model):
        if model not in 'cargo trucks'.split():
            raise NameError(f'The model {model} is not valid.')
        Model = Cargo if model == 'cargo' else Truck
        return [Model(_id, **data) for _id, data in enumerate(get_csv_reader(model), 1)]

    @property
    def best_combo(self):
        if self._best_combo:
            return self._best_combo
        self._process()
        return self._best_combo

    def _create_combinations(self):
        return [Combination(truck, cargo) for cargo in self.cargos for truck in self.trucks]

    def get_closer_trucks_list(self, cargo_id):
        combinations = filter(lambda x: x.cargo.id == cargo_id, self.combinations)
        return sorted(combinations, key=lambda x: x.distance_to_load)

    def _get_closer_combinations(self):
        for cargo in self.cargos:
            yield self.get_closer_trucks_list(cargo.id)

    def _get_filtered_combinations(self):
        for combination in self.closer_combinations:
            yield list(filter(
                lambda x: x.distance_to_load < combination[0].distance_to_load + self.threshold, combination
            ))

    def _create_combos(self):
        found = False
        while not found:
            filtered_ids = [comb.id for comb in chain.from_iterable(self._get_filtered_combinations())]
            all_combinations = combinations_with_replacement(filtered_ids, self.CARGO_COUNT)
            for combination in all_combinations:
                cargos, trucks = set(), set()
                for cargo, truck in (code.split(',') for code in combination):
                    cargos.add(cargo), trucks.add(truck)
                if len(cargos) == self.CARGO_COUNT and len(trucks) == self.CARGO_COUNT:
                    valid_combo = CombinationCombo(*list(filter(lambda x: x.id in combination, self.combinations)))
                    self.combos.append(valid_combo)
                    found = True
            if not found:
                self.threshold += self.threshold

    def _process(self):
        self._create_combos()
        self.combos.sort(key=lambda x: x.total_distance)
        self._best_combo = self.combos[0]

    def print_all_combos(self, limit=5, verbose=True):
        for combo in self.combos[:limit]:
            print(combo)
            if verbose:
                combo.print_combinations()

    def print_best_combo(self):
        print(self.best_combo)
        self.best_combo.print_combinations()
