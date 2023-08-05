from src.entity.domain import Domain


class Variable:
    def __init__(self, symbol, name, unit, domain_type, domain_range):
        self.symbol = symbol
        self.name = name
        self.unit = unit
        self.domain = Domain(domain_type, domain_range)

    def __str__(self):
        return f"{self.name} ({self.unit})"

    def __repr__(self):
        return f"Variable(symbol={self.symbol}, name={self.name}, unit={self.unit}, domain={self.domain})"

    def is_valid_value(self, value):
        return self.domain.is_valid_value(value)

    def get_symbol_and_unit(self):
        return f"{self.symbol} ({self.unit})"

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'name': self.name,
            'unit': self.unit,
            'domain_type': self.domain.type,
            'domain_range': self.domain.range
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            symbol=data['symbol'],
            name=data['name'],
            unit=data['unit'],
            domain_type=data['domain_type'],
            domain_range=data['domain_range']
        )
