class PrEDIctionData:

    def __init__(self):
        self.time_amount = None
        self.time_unit = None
        self.time = None
        self.mean = None
        self.min = None
        self.max = None
        self.std = None
        self.delta_time = None
        self.values = dict()

    def set_time_amount(self, time_amount):
        self.time_amount = time_amount

    def set_time_unit(self, time_unit):
        self.time_unit = time_unit

    def get_time_amount(self):
        return self.time_amount

    def get_time_unit(self):
        return self.time_unit
        
    def set_time(self, time):
        self.time = time

    def set_mean(self, mean):
        self.mean = mean

    def set_min(self, min):
        self.min = min

    def set_max(self, max):
        self.max = max

    def set_std(self, std):
        self.std = std

    def set_delta_time(self, delta_time):
        self.delta_time = delta_time

    def add_values(self, time, values):
        self.values[time] = values

    def get_time(self):
        return self.time

    def get_mean(self):
        return self.mean

    def get_min(self):
        return self.min

    def get_max(self):
        return self.max

    def get_std(self):
        return self.std

    def get_delta_time(self):
        return self.delta_time
        
    def get_values(self, time):
        return self.values.get(time)

    def get_values(self):
        return self.values
