import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import mysql.connector
import sys

# # Connection
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password=""
# )
# mycursor = mydb.cursor()

# # queries
# sql_queries = [
#     "DROP DATABASE IF EXISTS python_assignment_chishti",
#     "CREATE DATABASE python_assignment_chishti",
#     "CREATE TABLE train (id INT AUTO_INCREMENT PRIMARY KEY, x float, y1 float, y2 float, y3 float, y4 float)",
#     "CREATE TABLE test (id INT AUTO_INCREMENT PRIMARY KEY, x int(255), y int(255))",
#     "CREATE TABLE best_fit_func (id INT AUTO_INCREMENT PRIMARY KEY, x int(255), y int(255))",
#     "CREATE TABLE mapping (id INT AUTO_INCREMENT PRIMARY KEY, x int(255), y int(255), a int(255), b int(255), deviation int(255))",
#     "CREATE TABLE ideal (id INT AUTO_INCREMENT PRIMARY KEY, x int(255))",
#     *[f"ALTER TABLE ideal ADD COLUMN y{i+1} int;" for i in range(0, 50)]    
# ]
# mycursor.execute(sql_queries[0])
# mycursor.execute(sql_queries[1])

mydb_1 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="python_assignment_chishti"
)

mycursor_1 = mydb_1.cursor()

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
    # print("X : ",x_train)
    # print("Y : ",y_train)
    print("Y Train : ",y_train)
    # print("ideal func :",ideal_functions[1])
    
    for y in y_train:
        if j < 4:
            for y_ideal in ideal_functions:
                params, _ = curve_fit(ideal_function, x_train, y_train[:, j])  # Fit only the first column of y_train
                y_pred = ideal_function(x_train, *params)
                sum_squared_deviations = np.sum((y_train[:, j] - y_pred) ** 2)  # Calculate deviation only for the first column
                
                if sum_squared_deviations < min_sum_squared_deviations:
                    min_sum_squared_deviations = sum_squared_deviations
                    best_function_params = params
            print("J :",j)
            j = j+1
            best_functions.append(best_function_params)
    # best_functions.append(best_function_params)
    print("Best :",best_functions)
    return best_functions

# Load training dataset (A) and ideal functions dataset (C)
x_train, y_train = load_data("train.csv")
ideal_functions = load_data("ideal.csv")

sql = "INSERT INTO train (x, y1, y2, y3, y4) VALUES (%s, %s, %s, %s)"
val = [
  (x_train, y_train[0], y_train[1], y_train[2], y_train[3])
]
mycursor_1.executemany(sql, val)

# Choose the four best fitting ideal functions
chosen_functions = fit_ideal_functions((x_train, y_train), ideal_functions)
print("Params : ",chosen_functions)
# sys.exit()
print("Chosen ideal function parameters:")
for i, params in enumerate(chosen_functions):
    print(f"Ideal Function {i+1}: x={params[0]}, y={params[1]}")
