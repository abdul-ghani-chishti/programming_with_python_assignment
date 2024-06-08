import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import mysql.connector
from mysql.connector import Error
import sys
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool

mydb_1 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="python_assignment_chishti"
)

mycursor_1 = mydb_1.cursor()
mycursor_1.execute("show databases")
databases = mycursor_1.fetchall()
database_name = [ i[0] for i in databases ]

if 'python_assignment_chishti' in database_name:
    print('true')
else:
    print('Database not found, First run queries.py on terminal !')
    sys.exit()

# Load data from CSV files to veriables
def load_data(file_path):
    data = pd.read_csv(file_path)
    x = data['x'].values
    y_columns = [col for col in data.columns if col.startswith('y')]
    y_values = data[y_columns].values
    return x, y_values

# ideal function
def ideal_function(x, a, b):
    return a * x + b

# Fit ideal function to training data
def fit_ideal_functions(training_data, ideal_functions):
    best_functions = []
    min_sum_squared_deviations = float('inf')
    min_sum_squared_deviations_arry = []
    x_train, y_train = training_data

    j = 0
    for y in y_train:
        if j < 4:
            for y_ideal in ideal_functions:
                # Fit only the first column of y_train
                params, _ = curve_fit(ideal_function, x_train, y_train[:, j])
                y_pred = ideal_function(x_train, *params)
                # Calculate deviation only for the first column
                sum_squared_deviations = np.sum((y_train[:, j] - y_pred) ** 2)

                if sum_squared_deviations < min_sum_squared_deviations:
                    min_sum_squared_deviations = sum_squared_deviations
                    best_function_params = params
            j = j+1
            best_functions.append(best_function_params)
            min_sum_squared_deviations_arry.append(min_sum_squared_deviations)
    return best_functions,min_sum_squared_deviations_arry
    # put these values into the best_fit_function table

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
    # print(mappings[0])
    # sys.exit()
    return mappings
    # put these values into the mapping table

# Load training dataset (A) and ideal functions dataset (C) and test dataset (B)
x_train, y_train = load_data("train.csv")
ideal_functions = load_data("ideal.csv")
x_test, y_test = load_data("test.csv")

try:
    train_data_list = [
        (x, y1, y2, y3, y4)
        for x, y1, y2, y3, y4 in zip(x_train, y_train[:, 0], y_train[:, 1], y_train[:, 2], y_train[:, 3])
    ]
    mycursor_1.executemany(
        "INSERT INTO train (x, y1, y2, y3, y4) VALUES (%s, %s, %s, %s, %s)",
        train_data_list
    )
    mydb_1.commit()

    test_data_list = [
        (x, y)
        for x, y in zip(x_test, y_test[:, 0])
    ]
    mycursor_1.executemany(
        "INSERT INTO test (x, y) VALUES (%s, %s)",
        test_data_list
    )
    mydb_1.commit()

    x_ideal, y_ideal = ideal_functions
    ideal_values = [
        (x, *y_row)
        for x, y_row in zip(x_ideal, y_ideal)
    ]
    mycursor_1.executemany(
        "INSERT INTO ideal (x, " + ", ".join(
            [f"y{i+1}" for i in range(50)]) + ") VALUES (" + ", ".join(["%s"] * 51) + ")",
        ideal_values
    )
    mydb_1.commit()

    print("Data insertion completed successfully.")
except Error as e:
    print(f"Something Went Wrong or maybe database got crash !!! {e}")
finally:
    print("Enjoy !")

# Choose the four best fitting ideal functions
chosen_functions = fit_ideal_functions((x_train, y_train), ideal_functions)

# Map test data to chosen ideal functions
mappings = map_test_data((x_test, y_test), chosen_functions[0])

print("Chosen ideal function parameters:")
print("S.No        x                    y                chosen_val")
for i, params in enumerate(chosen_functions[0]):
    print(f" {i+1}: {params[0]}, {params[1]}, {chosen_functions[1][i]}")
    data_to_insert = [(params[0], params[1], chosen_functions[1][i])]
    mycursor_1.executemany(
        "INSERT INTO best_fit_func (x,y,choosen_func) VALUES (%s, %s, %s)", data_to_insert)    
mydb_1.commit()

print()
print("Mappings:")
print()
print(" x       y        Best fit (A)     Best fit  (B)      Deviation")
for i, (x, y, best_fit_params, deviation) in enumerate(mappings):
    if best_fit_params is not None:
        print(x, y[0], best_fit_params[0], best_fit_params[1], deviation[0])
        data_to_insert = [(x, y[0], best_fit_params[0], best_fit_params[1], deviation[0])]
        mycursor_1.executemany("INSERT INTO mapping (x,y,ideal_x,ideal_y,deviation) VALUES (%s, %s, %s, %s, %s)", data_to_insert)
    else:
        print(f"Data point {
              i+1}: x={x}, y={y}, No best fit found within the deviation threshold")
mydb_1.commit()

# Graphing
def plot_data_with_bokeh(x_train, y_train, x_test, y_test, chosen_functions, mappings):
    try:
        p = figure(title="Training Data, Ideal Functions, Test Data, and Mappings",
            x_axis_label='x', y_axis_label='y', width=800, height=600)
        
        # Plot training data
        for i in range(y_train.shape[1]):
            p.scatter(x_train, y_train[:, i], legend_label=f'Training y{i+1}',color='green', size=6, alpha=0.6)
        
        # Plot ideal functions
        x_range = np.linspace(min(x_train), max(x_train), 500)
        for i, params in enumerate(chosen_functions[0]):
            y_range = ideal_function(x_range, *params)
            p.line(x_range, y_range, legend_label=f'Ideal Function {i+1}',color='pink', line_width=2)
        
        # Plot test data
        for i in range(y_test.shape[1]):
            p.scatter(x_test, y_test[:, i], legend_label=f'Test Data y{i+1}', color='black', size=6, alpha=0.6)

        # Plot mappings with deviation
        mapped_x = [x for x, y, function_idx,
                    deviation in mappings if function_idx is not None]
        
        mapped_y = [y for x, y, function_idx,
                    deviation in mappings if function_idx is not None]
        deviations = [deviation for x, y, function_idx,
                    deviation in mappings if function_idx is not None]
        source = ColumnDataSource(data=dict(x=mapped_x, y=mapped_y, deviation=deviations))
        
        p.scatter('x', 'y', source=source, color='red', size=10,
                alpha=0.6, legend_label='Mapped Test Data')

        hover = HoverTool()
        hover.tooltips = [("x", "@x"), ("y", "@y"), ("deviation", "@deviation")]
        p.add_tools(hover)

        p.legend.location = "top_left"
        output_file("data_analysis.html")
        show(p)
    except Error as e:
        print(f"Wrong ! {e}")

# Plot the data using Bokeh
plot_data_with_bokeh(x_train, y_train, x_test, y_test,
                     chosen_functions, mappings)
