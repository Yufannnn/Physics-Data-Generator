import sympy
from src.util.constant_handler import ConstantHandler


class Formula:
    def __init__(self, name, equation, independent_variables, dependent_variable):
        self.name = name
        self.equation = equation
        self.independent_variables = independent_variables
        self.dependent_variable = dependent_variable

    def __str__(self):
        return (f"{self.name}: {self.equation}, Independent Variables: "
                f"{', '.join(str(v) for v in self.independent_variables)}, Dependent Variable: "
                f"{self.dependent_variable}")

    def __repr__(self):
        return (f"Formula(name={self.name}, equation={self.equation}, "
                f"independent_variables={self.independent_variables}, dependent_variable={self.dependent_variable})")

    def __eq__(self, other):
        if isinstance(other, Formula):
            return self.name == other.name and self.equation == other.equation
        return False

    def get_name_with_underline(self):
        return self.name.replace(" ", "_").replace(":", "")

    def calculate_data_point(self, values):
        if len(values) != len(self.independent_variables):
            raise ValueError("Number of values must match the number of independent variables.")

        # Create a dictionary to store the variable values
        variable_values = {var.symbol: value for var, value in zip(self.independent_variables, values)}

        # Replace constants in the equation with their values
        for var_symbol, value in variable_values.items():
            if isinstance(value, str) and value in ConstantHandler.get_constant_value(var_symbol):
                variable_values[var_symbol] = ConstantHandler.get_constant_value(value)

        try:
            # Use simplify to convert the equation to a sympy expression
            equation_expr = sympy.sympify(self.equation)

            # Substitute the variable values into the expression
            result = equation_expr.subs(variable_values)
            return result.evalf()  # Evaluate the expression to get the numerical result
        except Exception as e:
            raise ValueError(f"Error calculating the data point: {e}")

    def generate_random_data_point(self, bound=10000):
        random_values = [var.domain.get_random_input(bound) for var in self.independent_variables]

        result = [self.calculate_data_point(random_values)]
        for random_value in random_values:
            result.append(random_value)

        return result

    def get_variable_symbol_with_units(self):
        result = [f"{self.dependent_variable.symbol} ({self.dependent_variable.unit})"]
        for var in self.independent_variables:
            result.append(f"{var.symbol} ({var.unit})")
        return result

