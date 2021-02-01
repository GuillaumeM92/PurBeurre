from db_class import *

db.drop()
db.create()   # dropping, creating, and using the DB
db.use()

db.create_table(products_table_name, products_table_columns)   # creating the products table
db.inject_products()   # injecting the products table using OFF API

db.create_table(categories_table_name, categories_table_columns)   # creating the categories table
db.inject_categories()   # injecting the products table using OFF API

db.create_table(link_table_name, link_table_columns)
db.inject_link_table()

db.create_table(suggestions_table_name, suggestions_table_columns)   # creating the suggestions table

db.db.commit()   # committing changes to the database
