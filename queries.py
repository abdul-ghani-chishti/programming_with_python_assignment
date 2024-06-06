import mysql.connector
import sys
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

mycursor = mydb.cursor()

sql_queries = [
    "DROP DATABASE IF EXISTS python_assignment_chishti",
    "CREATE DATABASE python_assignment_chishti",
    "CREATE TABLE train (id INT AUTO_INCREMENT PRIMARY KEY, x float, y1 float, y2 float, y3 float, y4 float)",
    "CREATE TABLE test (id INT AUTO_INCREMENT PRIMARY KEY, x float, y float)",
    "CREATE TABLE best_fit_func (id INT AUTO_INCREMENT PRIMARY KEY, x float, y float)",
    "CREATE TABLE mapping (id INT AUTO_INCREMENT PRIMARY KEY, x float, y float, a float, b float, deviation float)",
    "CREATE TABLE ideal (id INT AUTO_INCREMENT PRIMARY KEY, x float)",
    *[f"ALTER TABLE ideal ADD COLUMN y{i+1} float;" for i in range(0, 50)]    
]

mycursor.execute(sql_queries[0])
mycursor.execute(sql_queries[1])

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
