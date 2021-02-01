# Connecting to the database

# importing 'mysql.connector'
import mysql.connector

# connection parameters
db = mysql.connector.connect(    # connecting to the database using 'connect()' method
    host = "localhost",
    user = "root",
    passwd = "Veanip206",
)

# creating an instance of the 'cursor' class which is used to execute the SQL statements in Python
cursor = db.cursor()

# creating the database
cursor.execute("CREATE DATABASE pur_beurre_db")

# entering pur beurre database
cursor.execute("USE pur_beurre_db")

# creating pur beurre table
cursor.execute("CREATE TABLE pur_beurre_table (id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT, nom_aliment VARCHAR(64) NOT NULL, catégories VARCHAR(64) NOT NULL, marques VARCHAR(64) NOT NULL, ingrédients TEXT NOT NULL, additifs TEXT NULL, allergènes TEXT NULL, notes_nutritionnelles VARCHAR(8) NOT NULL, magasins VARCHAR(64) NOT NULL, lien_OFF VARCHAR(128) NOT NULL, PRIMARY KEY (id))")

# displaying the content of pur beurre table
cursor.execute("DESCRIBE pur_beurre_table")

# fetching all the rows from the last executed statement
fetch = cursor.fetchall()

# printing the fetched lines
print(fetch)









