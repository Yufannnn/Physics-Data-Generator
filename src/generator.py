import os
import csv
import random

def linear_equation_generator(num_points, m_range, b_range):
    data_points = []

    for _ in range(num_points):
        m = random.uniform(m_range[0], m_range[1])
        b = random.uniform(b_range[0], b_range[1])

        x = random.uniform(-10, 10)  # Assuming x range from -10 to 10 for this example

        y = m * x + b
        data_points.append((x, y))

    # Sort the data points based on the 'x' value before saving
    data_points.sort(key=lambda point: point[0])

    return data_points

def save_data_to_csv(data_points):
    csv_file_path = os.path.join("../data", "generated_data.csv")

    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y'])
        writer.writerows(data_points)

# Create the data folder if it does not exist
if not os.path.exists("data"):
    os.makedirs("data")

# Example usage
num_data_points = 10
m_range = (-5, 5)  # Range of m values
b_range = (-10, 10)  # Range of b values

data_points = linear_equation_generator(num_data_points, m_range, b_range)
print(data_points)

# Save the data points to a CSV file in the data subfolder
save_data_to_csv(data_points)
