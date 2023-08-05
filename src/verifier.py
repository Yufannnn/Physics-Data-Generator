import sys

import numpy as np
import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, \
    QDesktopWidget, QComboBox, QLineEdit
from matplotlib import pyplot as plt
import statsmodels.api as sm

from src.formula_loader import FormulaLoader
from src.util.constant_handler import ConstantHandler


class ModelVerifier(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load formulas using FormulaLoader
        formula_loader = FormulaLoader('../data/formulae/formulae.json')
        self.formulas = formula_loader.load_formulas()

        # Set up the main window
        self.setWindowTitle('Model Verifier')
        self.setGeometry(100, 100, 400, 250)

        # Center the window on the screen
        self.center_window()

        # set Icon for the window
        self.setWindowIcon(QIcon('../res/images/icon.png'))

        # Create a layout
        layout = QVBoxLayout()

        # Create a label
        label = QLabel('Select a formula:')
        layout.addWidget(label)

        # Create a dropdown list (QComboBox) to display the formula titles
        self.formula_dropdown = QComboBox()
        for formula in self.formulas:
            self.formula_dropdown.addItem(formula.name)
        self.formula_dropdown.currentIndexChanged.connect(self.on_formula_selected)
        layout.addWidget(self.formula_dropdown)

        # Create a label to display the selected formula
        self.selected_formula_label = QLabel()
        layout.addWidget(self.selected_formula_label)

        # Create a label and text input for the regressed model
        model_label = QLabel('Enter the Regressed Model:')
        layout.addWidget(model_label)

        self.model_input = QLineEdit()
        layout.addWidget(self.model_input)

        # Create a button to verify the model
        verify_button = QPushButton('Verify Model')
        verify_button.clicked.connect(self.calculate_error)
        layout.addWidget(verify_button)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_formula_selected(self):
        # Get the selected formula index
        selected_index = self.formula_dropdown.currentIndex()

        if 0 <= selected_index < len(self.formulas):
            # Display the selected formula in the label
            selected_formula = self.formulas[selected_index]
            self.selected_formula_label.setText(f"Selected Formula: {selected_formula.name}\n"
                                                f"Equation: {selected_formula.equation}")

            # Display the symbol and unit for each independent variable
            variable_info = "Independent Variables:\n"
            for variable in selected_formula.independent_variables:
                variable_info += f"{variable.name} : {variable.symbol} ({variable.unit})\n"

            # Display the symbol and unit for the dependent variable
            variable_info += f"{selected_formula.dependent_variable.name} : {selected_formula.dependent_variable.symbol} " \
                             f"({selected_formula.dependent_variable.unit})\n"

            self.selected_formula_label.setText(f"{self.selected_formula_label.text()}\n{variable_info}")

    def calculate_results(self):
        # Get the selected formula name from the drop-down list
        selected_formula = self.formula_dropdown.currentText()
        # Replace spaces with underscores and remove special characters
        selected_formula = selected_formula.replace(' ', '_').replace(':', '')

        # Figure out the file path based on the selected formula name
        file_path = f'../data/testing_data/{selected_formula}.csv'

        loaded_data = pd.read_csv(file_path)
        # get the first column of the data as the dependent variable
        expected_result = loaded_data[loaded_data.columns[0]].tolist()

        independent_variables = [column_name for column_name in loaded_data.columns[1:]]
        independent_variables = [variable.split(' ')[0] for variable in independent_variables]

        input_variables = loaded_data[loaded_data.columns[1:]].values.tolist()

        regressed_model = self.model_input.text()
        regressed_model = self.clean_formula(regressed_model)

        regressed_result = []

        # For each row in the input variables, replace the independent variables with the values in the row
        for row in input_variables:
            # Make a copy of the regressed model
            regressed_model_copy = regressed_model

            # Replace the independent variables with the values in the row, add a bracket to each value
            for i in range(len(independent_variables)):
                regressed_model_copy = regressed_model_copy.replace(independent_variables[i], f"({str(row[i])})")

            print(regressed_model_copy)
            # Evaluate the regressed model
            regressed_result.append(eval(regressed_model_copy))

        # Calculate the number of data points (n) and the number of independent variables (p)

        return expected_result, regressed_result

    def clean_formula(self, formula):
        formula = formula.replace('^', '**')

        if '=' in formula:
            formula = formula.split('=')[1]

        if '≈' in formula:
            formula = formula.split('≈')[1]

        formula = ConstantHandler.handle_constant_in_equation(formula)

        return formula

    def calculate_error(self):
        # Call the calculate_results function to get the expected and regressed results
        expected_result, fitted_result = self.calculate_results()

        print(f"Expected Result: {expected_result}")
        print(f"Fitted Result: {fitted_result}")

        # Convert the results to numpy arrays for easier computation
        expected_result = np.array(expected_result)
        fitted_result = np.array(fitted_result)

        # Calculate the Residuals
        residuals = fitted_result - expected_result

        print(f"Residuals: {residuals}")

        SSR = np.sum((fitted_result - expected_result) ** 2)
        SST = np.sum((expected_result - np.mean(expected_result)) ** 2)

        print(f"SSR: {SSR}")
        print(f"SST: {SST}")

        # Calculate the R-squared value
        r_squared = 1 - (SSR / SST)

        print(f"R-squared: {r_squared}")

        # Plot the graphs
        self.plot_graphs(residuals, fitted_result)

        return residuals, r_squared

    def plot_graphs(self, residuals, fitted_result):
        # Residuals vs. Fitted Values Plot
        plt.figure(figsize=(8, 6))
        plt.scatter(fitted_result, residuals, c='blue', marker='o', edgecolors='black')
        plt.axhline(y=0, color='red', linestyle='--')
        plt.xlabel('Fitted Values')
        plt.ylabel('Residuals')
        plt.title('Residuals vs. Fitted Values Plot')
        # tight layout
        plt.tight_layout()
        plt.show()

        # Normal Q-Q Plot
        sm.qqplot(residuals, line='s')
        plt.xlabel('Theoretical Quantiles')
        plt.ylabel('Standardized Residuals')
        plt.title('Normal Q-Q Plot of Residuals')
        # tight layout
        plt.tight_layout()
        plt.show()

    def center_window(self):
        # Get the size of the screen
        screen_geometry = QDesktopWidget().screenGeometry()

        # Get the size of the window
        window_geometry = self.frameGeometry()

        # Calculate the center position of the window
        center_position = screen_geometry.center() - window_geometry.center()

        # Move the window to the center position
        self.move(center_position)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModelVerifier()
    window.show()
    sys.exit(app.exec_())
