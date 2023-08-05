from src.entity.formula import Formula
from src.entity.variable import Variable
from src.formula_loader import FormulaLoader

if __name__ == "__main__":
    file_name = '../data/formulae/formulae.json'
    # create the formula folder and file if it does not exist
    open(file_name, 'a').close()

    K_spring = Variable('k_spring', 'Spring constant', 'N/m', 'real', '[0, inf]')
    x = Variable('x', 'Displacement', 'm', 'real', '[-inf, inf]')
    U = Variable('U', 'Potential energy', 'J', 'real', '[-inf, inf]')

    q = Variable('q', 'Charge', 'C', 'real', '[-inf, inf]')
    C = Variable('C', 'Capacitance', 'F', 'real', '[0, inf]')
    V_epsilon = Variable('V_epsilon', 'Electric potential', 'V', 'real', '[-inf, inf]')

    # Create the formula
    spring_potential_formula = Formula('I.14.4: Potential Energy of a Spring', '0.5 * k_spring * x ** 2',
                                       [K_spring, x], U)

    capacitance_formula = Formula('I.25.13: Capacitance', 'q / C', [q, C], V_epsilon)

    # Create a formula loader
    formula_loader = FormulaLoader(file_name)
    formula_loader.add_formula(capacitance_formula)
