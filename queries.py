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
    "CREATE TABLE train (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))",
    "CREATE TABLE ideal (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))",
    "CREATE TABLE test (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))",
    "CREATE TABLE best_fit_func (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))",
    "CREATE TABLE result (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))"]

mycursor.execute(sql_queries[0])

# mycursor.execute("CREATE DATABASE python_assignment_chishti") 

mydb_1 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="python_assignment_chishti"
)

mycursor_1 = mydb_1.cursor()

for i, table in enumerate(sql_queries):
    if i > 0:
        mycursor_1.execute(table)
        print("Database and Tables Created Successfully !")
