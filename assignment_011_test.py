import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import mysql.connector
import sys

# Load data from CSV files
def load_data(file_path):
    data = pd.read_csv(file_path)
    x = data['x'].values
    y_columns = [col for col in data.columns if col.startswith('y')]
    y_values = data[y_columns].values
    return x, y_values

# Define ideal function
def ideal_function(x, a, b):
    return a * x + b

# Fit ideal function to training data
def fit_ideal_functions(training_data, ideal_functions):
    best_functions = []
    min_sum_squared_deviations = float('inf')
    x_train, y_train = training_data

    j = 0    
    for y in y_train:
        if j < 4:
            for y_ideal in ideal_functions:
                params, _ = curve_fit(ideal_function, x_train, y_train[:, j])  # Fit only the first column of y_train
                y_pred = ideal_function(x_train, *params)
                sum_squared_deviations = np.sum((y_train[:, j] - y_pred) ** 2)  # Calculate deviation only for the first column
                
                if sum_squared_deviations < min_sum_squared_deviations:
                    min_sum_squared_deviations = sum_squared_deviations
                    best_function_params = params
            j = j+1
            best_functions.append(best_function_params)
    return best_functions

# Map test data to chosen ideal functions
def map_test_data(test_data, chosen_functions):
    x_test, y_test = test_data
    mappings = []

    for x, y in zip(x_test, y_test):
        deviations = []
        for params in chosen_functions:
            y_pred = ideal_function(x, *params)
            deviation = np.abs(y - y_pred)
            deviations.append(deviation)
        min_deviation = min(deviations)
        if min_deviation < np.sqrt(2) * np.max(deviations):
            best_fit_index = deviations.index(min_deviation)
            best_fit_params = chosen_functions[best_fit_index]
            mappings.append((x, y, best_fit_params, min_deviation))
        else:
            mappings.append((x, y, None, None))
    return mappings

# Load training dataset (A) and ideal functions dataset (C)
x_train, y_train = load_data("train.csv")
ideal_functions = load_data("ideal.csv")

# Choose the four best fitting ideal functions
chosen_functions = fit_ideal_functions((x_train, y_train), ideal_functions)

# Load test dataset (B)
x_test, y_test = load_data("test.csv")

# Map test data to chosen ideal functions
mappings = map_test_data((x_test, y_test), chosen_functions)

print("Chosen ideal function parameters:")
for i, params in enumerate(chosen_functions):
    print(f"Ideal Function {i+1}: x={params[0]}, y={params[1]}")

print()
print("Mappings:")
print()
print("x, y, Best fit parameters (A), Best fit parameters (B), Deviation")
for i, (x, y, best_fit_params, deviation) in enumerate(mappings):
    if best_fit_params is not None:
        print(x,y[0],best_fit_params[0],best_fit_params[1],deviation[0])
        # print(f"Data point {i+1}: x={x}, y={y}, Best fit parameters: a={best_fit_params[0]}, b={best_fit_params[1]}, Deviation: {deviation}")
    else:
        print(f"Data point {i+1}: x={x}, y={y}, No best fit found within the deviation threshold")
    # print("M : ",mappings)