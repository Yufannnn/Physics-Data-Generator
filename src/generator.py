import os
import sys

import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QComboBox, QWidget, QDesktopWidget, \
    QSpinBox, QPushButton
from src.formula_loader import FormulaLoader


class PhysicsDataGenerator(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load formulas using FormulaLoader
        formula_loader = FormulaLoader('data/formulae/formulae.json')
        self.formulas = formula_loader.load_formulas()

        # Set up the main window
        self.setWindowTitle('Physics Data Generator')
        self.setGeometry(100, 100, 400, 300)

        # Center the window on the screen
        self.center_window()

        # set Icon for the window
        self.setWindowIcon(QIcon('res/images/icon.png'))

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

        # Create a QLabel and QSpinBox to select the number of data points to be generated
        data_points_label = QLabel('Select number of data points:')
        layout.addWidget(data_points_label)

        self.data_points_spinbox = QSpinBox()
        self.data_points_spinbox.setMinimum(1)
        self.data_points_spinbox.setMaximum(10000)
        layout.addWidget(self.data_points_spinbox)

        # Create a QLabel and QSpinBox to select the boundary value for infinity (inf option)
        inf_boundary_label = QLabel('Select boundary value for infinity:')
        layout.addWidget(inf_boundary_label)

        self.inf_boundary_spinbox = QSpinBox()
        self.inf_boundary_spinbox.setMinimum(1)
        self.inf_boundary_spinbox.setMaximum(10000)
        layout.addWidget(self.inf_boundary_spinbox)

        # to choose whether generate for training or testing
        self.training_or_testing = QComboBox()
        self.training_or_testing.addItem("Training")
        self.training_or_testing.addItem("Testing")
        layout.addWidget(self.training_or_testing)

        # Create a QPushButton to initiate data generation
        generate_button = QPushButton('Generate Data')
        generate_button.clicked.connect(self.generate_data_points)
        layout.addWidget(generate_button)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def center_window(self):
        # Get the size of the screen
        screen_geometry = QDesktopWidget().screenGeometry()

        # Get the size of the window
        window_geometry = self.frameGeometry()

        # Calculate the center position of the window
        center_position = screen_geometry.center() - window_geometry.center()

        # Move the window to the center position
        self.move(center_position)

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

    def generate_data_points(self):
        selected_formula_index = self.formula_dropdown.currentIndex()
        if 0 <= selected_formula_index < len(self.formulas):
            selected_formula = self.formulas[selected_formula_index]
            num_data_points = self.data_points_spinbox.value()
            inf_boundary = self.inf_boundary_spinbox.value()
            print(f"Generating {num_data_points} data points for formula: {selected_formula.name}")
            print(f"Boundary value for infinity: {inf_boundary}")

            generated_data_points = []
            # Add your data generation logic here
            for _ in range(num_data_points):
                generated_data_points.append(selected_formula.generate_random_data_point(inf_boundary))
            generated_data_points = self.sort_data_points(generated_data_points)
            variable_info = selected_formula.get_variable_symbol_with_units()
            data_frame = pd.DataFrame(generated_data_points, columns=variable_info)

            # Save the data points to a csv file
            self.save_data_points(data_frame, selected_formula.get_name_with_underline(), self.is_training())

    def is_training(self):
        if self.training_or_testing.currentText() == "Training":
            return True
        else:
            return False

    def sort_data_points(self, generated_data):
        # sort the data points by the independent variable
        sorted_data_points = sorted(generated_data, key=lambda x: x[0])
        return sorted_data_points

    def save_data_points(self, data_frame, formula_name, is_training_data=True):
        if is_training_data:
            file_name = 'data/training_data/' + formula_name + '.csv'
        else:
            file_name = 'data/testing_data/' + formula_name + '.csv'

        # Check if the file exists and contains data before reading
        if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
            existing_data_points = pd.read_csv(file_name)
        else:
            # If the file does not exist or is empty, create an empty DataFrame
            existing_data_points = pd.DataFrame()

        # append the new data points to the existing data points
        data_frame = pd.concat([existing_data_points, data_frame])
        # sort the data points by the independent variable
        data_frame = data_frame.sort_values(by=data_frame.columns[0])
        # save the data points to a csv file
        data_frame.to_csv(file_name, index=False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhysicsDataGenerator()
    window.show()
    sys.exit(app.exec_())
