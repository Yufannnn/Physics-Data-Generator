import os
import csv
import matplotlib.pyplot as plt

def plot_graph_from_csv(csv_file_path):
    x_values = []
    y_values = []

    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            x_values.append(float(row[0]))
            y_values.append(float(row[1]))

    plt.plot(x_values, y_values, 'bo-', label='Generated Data')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Generated Data Plot')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    data_file_path = os.path.join("../data", "generated_data.csv")
    if os.path.exists(data_file_path):
        plot_graph_from_csv(data_file_path)
    else:
        print("The data file does not exist. Please generate the data points first.")
