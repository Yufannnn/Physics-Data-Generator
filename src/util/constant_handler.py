import math
import re


class ConstantHandler:
    # Dictionary to store constants and their corresponding values
    constants = {
        'pi': math.pi,
        'e': math.e,
        'c': 299792458,  # Speed of light in vacuum (m/s)
        'G': 6.67430e-11,  # Gravitational constant (m^3/kg/s^2)
        'h': 6.62607015e-34,  # Planck constant (J*s)
        'k': 1.380649e-23,  # Boltzmann constant (J/K)
        'Na': 6.02214076e23,  # Avogadro's number (1/mol)
        'R': 8.314462618,  # Ideal gas constant (J/mol/K)
    }

    @staticmethod
    def handle_constant_in_equation(equation):
        for constant in ConstantHandler.get_constants_in_equation(equation):
            equation = ConstantHandler.replace_constant_in_equation(equation, constant)
        return equation

    @staticmethod
    def get_constants_in_equation(equation):
        return [constant for constant in ConstantHandler.constants.keys() if
                ConstantHandler.is_constant_in_equation(equation, constant)]

    @staticmethod
    def is_constant_in_equation(equation, constant):
        pattern = r"(?<![a-zA-Z0-9_])" + re.escape(constant) + r"(?![a-zA-Z0-9_])"
        return bool(re.search(pattern, equation))

    @staticmethod
    def replace_constant_in_equation(equation, constant):
        pattern = r"(?<![a-zA-Z0-9_])" + re.escape(constant) + r"(?![a-zA-Z0-9_])"
        return re.sub(pattern, str(ConstantHandler.get_constant_value(constant)), equation)

    @staticmethod
    def get_constant_value(constant):
        return ConstantHandler.constants.get(constant, None)
