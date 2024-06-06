import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import mysql.connector
from mysql.connector import Error
import sys
from bokeh.plotting import figure, output_file, show
import math

# mydb_1 = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="python_assignment_chishti"
# )

# mycursor_1 = mydb_1.cursor()

# # Load data from CSV files to veriables
# def load_data(file_path):
#     data = pd.read_csv(file_path)
#     x = data['x'].values
#     y_columns = [col for col in data.columns if col.startswith('y')]
#     y_values = data[y_columns].values
#     return x, y_values

# # ideal function
# def ideal_function(x, a, b):
#     return a * x + b

# # Fit ideal function to training data
# def fit_ideal_functions(training_data, ideal_functions):
#     best_functions = []
#     min_sum_squared_deviations = float('inf')
#     x_train, y_train = training_data

#     j = 0
#     for y in y_train:
#         if j < 4:
#             for y_ideal in ideal_functions:
#                 # Fit only the first column of y_train
#                 params, _ = curve_fit(ideal_function, x_train, y_train[:, j])
#                 y_pred = ideal_function(x_train, *params)
#                 # Calculate deviation only for the first column
#                 sum_squared_deviations = np.sum((y_train[:, j] - y_pred) ** 2)

#                 if sum_squared_deviations < min_sum_squared_deviations:
#                     min_sum_squared_deviations = sum_squared_deviations
#                     best_function_params = params
#             j = j+1
#             best_functions.append(best_function_params)
#     return best_functions
#     # put these values into the best_fit_function table

# # Map test data to chosen ideal functions
# def map_test_data(test_data, chosen_functions):
#     x_test, y_test = test_data
#     mappings = []

#     for x, y in zip(x_test, y_test):
#         deviations = []
#         for params in chosen_functions:
#             y_pred = ideal_function(x, *params)
#             deviation = np.abs(y - y_pred)
#             deviations.append(deviation)
#         min_deviation = min(deviations)
#         if min_deviation < np.sqrt(2) * np.max(deviations):
#             best_fit_index = deviations.index(min_deviation)
#             best_fit_params = chosen_functions[best_fit_index]
#             mappings.append((x, y, best_fit_params, min_deviation))
#         else:
#             mappings.append((x, y, None, None))
#     return mappings
#     # put these values into the mapping table


# # Load training dataset (A) and ideal functions dataset (C) and test dataset (B)
# x_train, y_train = load_data("train.csv")
# ideal_functions = load_data("ideal.csv")
# x_test, y_test = load_data("test.csv")

# try:
#     train_data_list = [
#         (x, y1, y2, y3, y4)
#         for x, y1, y2, y3, y4 in zip(x_train, y_train[:, 0], y_train[:, 1], y_train[:, 2], y_train[:, 3])
#     ]
#     mycursor_1.executemany(
#         "INSERT INTO train (x, y1, y2, y3, y4) VALUES (%s, %s, %s, %s, %s)",
#         train_data_list
#     )
#     mydb_1.commit()

#     test_data_list = [
#         (x, y)
#         for x, y in zip(x_test, y_test[:, 0])
#     ]
#     mycursor_1.executemany(
#         "INSERT INTO test (x, y) VALUES (%s, %s)",
#         test_data_list
#     )
#     mydb_1.commit()

#     x_ideal, y_ideal = ideal_functions
#     ideal_values = [
#         (x, *y_row)
#         for x, y_row in zip(x_ideal, y_ideal)
#     ]
#     mycursor_1.executemany(
#         "INSERT INTO ideal (x, " + ", ".join(
#             [f"y{i+1}" for i in range(50)]) + ") VALUES (" + ", ".join(["%s"] * 51) + ")",
#         ideal_values
#     )
#     mydb_1.commit()
    
#     print("Data insertion completed successfully.")
# except Error as e:
#     print("Something Went Wrong or maybe database got crash !!!")
# finally:
#     print("Enjoy !")

# # Choose the four best fitting ideal functions
# chosen_functions = fit_ideal_functions((x_train, y_train), ideal_functions)

# # Map test data to chosen ideal functions
# mappings = map_test_data((x_test, y_test), chosen_functions)

# print("Chosen ideal function parameters:")
# for i, params in enumerate(chosen_functions):
#     print(f"Ideal Function {i+1}: x={params[0]}, y={params[1]}")
#     data_to_insert = [(params[0], params[1])]
#     mycursor_1.executemany("INSERT INTO best_fit_func (x,y) VALUES (%s, %s)",data_to_insert)
    
# mydb_1.commit()

# print()
# print("Mappings:")
# print()
# print("x, y, Best fit parameters (A), Best fit parameters (B), Deviation")

# for i, (x, y, best_fit_params, deviation) in enumerate(mappings):
#     if best_fit_params is not None:
#         print(x, y[0], best_fit_params[0], best_fit_params[1], deviation[0])
#     else:
#         print(f"Data point {
#               i+1}: x={x}, y={y}, No best fit found within the deviation threshold")
