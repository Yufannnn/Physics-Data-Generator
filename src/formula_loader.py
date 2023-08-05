import json
from src.entity.formula import Formula
from src.entity.variable import Variable


class FormulaEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Variable):
            return o.to_dict()
        return super().default(o)


class FormulaLoader:
    def __init__(self, formula_file):
        self.formula_file = formula_file
        self.formulas = self.load_formulas()

    def load_formulas(self):
        try:
            with open(self.formula_file, 'r') as file:
                formulas_data = json.load(file)
                formulas = []
                for data in formulas_data:
                    name = data['name']
                    equation = data['equation']
                    independent_variables_data = data['independent_variables']
                    dependent_variable_data = data['dependent_variable']

                    independent_variables = [Variable.from_dict(v_data) for v_data in independent_variables_data]
                    dependent_variable = Variable.from_dict(dependent_variable_data)

                    formula = Formula(name, equation, independent_variables, dependent_variable)
                    formulas.append(formula)
                return formulas
        except FileNotFoundError:
            return []

    def save_formulas(self):
        formulas_data = []
        for formula in self.formulas:
            formula_data = {
                'name': formula.name,
                'equation': formula.equation,
                'independent_variables': formula.independent_variables,
                'dependent_variable': formula.dependent_variable
            }
            formulas_data.append(formula_data)
        with open(self.formula_file, 'w') as file:
            json.dump(formulas_data, file, indent=4, cls=FormulaEncoder)

    # prevent duplicate formulas
    def add_formula(self, formula):
        if formula not in self.formulas:
            self.formulas.append(formula)
            self.save_formulas()

    def get_formula(self, name):
        for formula in self.formulas:
            if formula.name == name:
                return formula
        return None

    def list_formulas(self):
        return self.formulas
