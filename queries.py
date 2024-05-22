import mysql.connector
import sys
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

mycursor = mydb.cursor()

# sql_queries = [
#     "DROP DATABASE IF EXISTS python_assignment_chishti",
#     "CREATE DATABASE python_assignment_chishti",
#     "CREATE TABLE train (id INT AUTO_INCREMENT PRIMARY KEY, x_value int(255), y1 int(255), y2 int(255), y3 int(255), y4 int(255))",
#     "CREATE TABLE test (id INT AUTO_INCREMENT PRIMARY KEY, x_value int(255), y_value int(255))",
#     "CREATE TABLE best_fit_func (id INT AUTO_INCREMENT PRIMARY KEY, x_value int(255), y_value int(255))",
#     "CREATE TABLE mapping (id INT AUTO_INCREMENT PRIMARY KEY, x_value int(255), y_value int(255), a int(255), b int(255), deviation int(255))"
# ]


sql_queries = [
    "DROP DATABASE IF EXISTS python_assignment_chishti",
    "CREATE DATABASE python_assignment_chishti",
    "CREATE TABLE ideal (id INT AUTO_INCREMENT PRIMARY KEY, x int(255))",
    *[f"ALTER TABLE ideal ADD COLUMN y{i+1} int;" for i in range(0, 50)],

]

mycursor.execute(sql_queries[0])
mycursor.execute(sql_queries[1])
# sys.exit()
mydb_1 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="python_assignment_chishti"
)

mycursor_1 = mydb_1.cursor()

for i, table in enumerate(sql_queries):
    if i > 1:
        mycursor_1.execute(table)

print("Database and Tables Created Successfully !")
