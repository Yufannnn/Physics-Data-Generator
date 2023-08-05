import random

class Domain:
    def __init__(self, domain_type, domain_range):
        self.type = domain_type
        self.range = domain_range

    def __repr__(self):
        return f"Domain(type={self.type}, range={self.range})"

    def is_valid_value(self, value):
        if self.type == 'real':
            bounds = self.range.strip('[]').split(',')
            lower_bound, upper_bound = float(bounds[0]), float(bounds[1])
            return lower_bound <= value <= upper_bound

        elif self.type == 'integer':
            if not isinstance(value, int):
                return False
            bounds = self.range.strip('[]').split(',')
            lower_bound, upper_bound = int(bounds[0]), int(bounds[1])
            return lower_bound <= value <= upper_bound

        return False

    def get_random_input(self, bound_for_inf=10000):
        if self.type == 'real':
            bounds = self.range.strip('[]').split(',')
            lower_bound, upper_bound = float(bounds[0]), float(bounds[1])
            if lower_bound == -float('inf'):
                lower_bound = -bound_for_inf
            if upper_bound == float('inf'):
                upper_bound = bound_for_inf
            return random.uniform(lower_bound, upper_bound)

        elif self.type == 'integer':
            bounds = self.range.strip('[]').split(',')
            lower_bound, upper_bound = int(bounds[0]), int(bounds[1])
            if lower_bound == -int('inf'):
                lower_bound = -bound_for_inf
            if upper_bound == int('inf'):
                upper_bound = bound_for_inf
            return random.randint(lower_bound, upper_bound)

        return None
