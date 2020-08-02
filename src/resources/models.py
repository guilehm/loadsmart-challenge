class Cargo:
    def __init__(self, kwargs):
        self.product = kwargs.pop('product')
        self.origin_city = kwargs.pop('origin_city')
        self.origin_state = kwargs.pop('origin_state')
        self.origin_lat = kwargs.pop('origin_lat')
        self.origin_lng = kwargs.pop('origin_lng')
        self.destination_city = kwargs.pop('destination_city')
        self.destination_state = kwargs.pop('destination_state')
        self.destination_lat = kwargs.pop('destination_lat')
        self.destination_lng = kwargs.pop('destination_lng')

    def __str__(self):
        return f'CARGO: [{self.origin_state} - {self.destination_state}] - {self.product}'


class Truck:
    def __init__(self, kwargs):
        self.truck = kwargs.pop('truck')
        self.city = kwargs.pop('city')
        self.state = kwargs.pop('state')
        self.lat = kwargs.pop('lat')
        self.lng = kwargs.pop('lng')

    def __str__(self):
        return f'TRUCK: {self.truck}'
