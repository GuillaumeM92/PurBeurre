import mysql.connector
import requests

products_table_name = "pur_beurre_produits"
products_table_columns = (
    "(numéro_produit SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, "
    "nom_aliment VARCHAR(256) NOT NULL, "
    "marque TEXT, "
    "ingrédients TEXT, "
    "allergènes TEXT, "
    "note_nutritionnelle VARCHAR(32), "
    "magasins VARCHAR(128), "
    "labels TEXT, "
    "lien_OFF VARCHAR(128))"
)

products_table_name_copy = "pur_beurre_produits_copie"


categories_table_name = "pur_beurre_catégories"
categories_table_columns = (
    "(numéro_catégorie SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, "
    "nom_catégorie VARCHAR(1024) NOT NULL)"
)

link_table_name = "pur_beurre_catégories_produits"
link_table_columns = (
    "(numéro_produit SMALLINT UNSIGNED NOT NULL, "
    "numéro_catégorie SMALLINT UNSIGNED NOT NULL, "
    "FOREIGN KEY (numéro_produit) REFERENCES pur_beurre_produits (numéro_produit) ON DELETE RESTRICT ON UPDATE CASCADE, "
    "FOREIGN KEY (numéro_catégorie) REFERENCES pur_beurre_catégories (numéro_catégorie) ON DELETE RESTRICT ON UPDATE CASCADE, "
    "PRIMARY KEY (numéro_produit, numéro_catégorie))"
)

suggestions_table_name = "pur_beurre_suggestions"
suggestions_table_columns = (
    "(id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, "
    "numéro_produit SMALLINT UNSIGNED NOT NULL, "
    "FOREIGN KEY (numéro_produit) REFERENCES pur_beurre_produits (numéro_produit) ON DELETE RESTRICT ON UPDATE CASCADE)"
)


class DataBase:
    def __init__(self, my_host, my_user, my_password, db_name):
        self.db = mysql.connector.connect(
            host=my_host, user=my_user, password=my_password
        )
        self.name = db_name
        self.cursor = self.db.cursor(
            buffered=True
        )  # creating an instance of the 'cursor' class to execute SQL statements from Python
        self.json_db = requests.get(
            "https://fr.openfoodfacts.org/cgi/search.pl?action=process&page_size=1000&json=True"
        ).json()
        self.json_categories = requests.get(
            "https://fr.openfoodfacts.org/categories&json=True"
        ).json()
        self.json_categories_list = []
        self.categories_limit = 28

    def drop(self):
        self.cursor.execute(
            "DROP DATABASE IF EXISTS {0}".format(self.name)
        )  # drops the previous db with same name if exists

    def create(self):
        self.cursor.execute("CREATE DATABASE {0}".format(self.name))  # creates a new db

    def use(self):
        self.cursor.execute("USE {0}".format(self.name))  # enters the newly created db

    def create_table(self, table_name, table_columns):  # creates the main table
        self.cursor.execute("CREATE TABLE {0} {1}".format(table_name, table_columns))

    def inject_products(
        self,
    ):  # reads the json data and inserts the desired values in the DB
        for product in self.json_db["products"]:
            try:
                insert = (
                    "INSERT INTO pur_beurre_produits (numéro_produit, nom_aliment, marque, ingrédients, "
                    "allergènes, note_nutritionnelle, magasins, labels, lien_OFF) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                )
                values = (
                    0,
                    product["product_name_fr"],
                    product["brands"],
                    product["ingredients_text_fr"],
                    product["allergens"],
                    product["nutrition_grades_tags"][0],
                    product["stores"],
                    product["labels"],
                    product["url"],
                )
            except KeyError:
                pass

            self.cursor.execute(insert, values)

    def inject_categories(self):
        index = 0
        for category in self.json_categories["tags"]:
            try:
                insert = "INSERT INTO pur_beurre_catégories (numéro_catégorie, nom_catégorie) VALUES (%s, %s)"
                values = (0, category["name"])
                self.cursor.execute(insert, values)
                index += 1
                self.json_categories_list.append(category["name"])
            except KeyError:
                pass
            if index == self.categories_limit:
                break

    def inject_link_table(self):
        for product in self.json_db["products"]:
            try:
                product_categories_list = (
                    product["categories"]
                    .replace("' ", "'")
                    .replace(", ", ",")
                    .split(",")
                )
                product_name = str(product["product_name_fr"])

                for category in product_categories_list:
                    if category in self.json_categories_list:
                        try:

                            self.cursor.execute(
                                'SELECT DISTINCT numéro_produit FROM pur_beurre_produits WHERE nom_aliment = "{0}" LIMIT 1'.format(
                                    product_name
                                )
                            )
                            resp = self.cursor.fetchone()
                            insert = "INSERT INTO pur_beurre_catégories_produits (numéro_produit, numéro_catégorie) VALUES (%s, %s)"
                            values = (
                                resp[0],
                                (self.json_categories_list.index(category)) + 1,
                            )
                            self.cursor.execute(insert, values)
                            continue

                        except (mysql.connector.errors.IntegrityError, TypeError):
                            pass

            except KeyError:
                pass


db = DataBase("localhost", "root", "Veanip", "pur_beurre_db")
