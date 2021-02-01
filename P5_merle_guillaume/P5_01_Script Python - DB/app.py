from db_class import db as database


class App:

    def __init__(self, db):
        self.running = True
        self.cursor = db.cursor
        self.db = db

    @staticmethod
    def welcome_text():
        print('\nBonjour, bienvenue dans le programme de suggestions nutritionnelles de Pur Beurre.\n')

    @staticmethod
    def menu_choice():
        print('Que souhaitez-vous faire ?\n\n1. Choisir un aliment à remplacer.\n2. Voir mes suggestions précédentes.\n'
              '3. Quitter l\'application\n\nEntrez un numéro et appuyez sur \'Entrée\' pour continuer :')

    @staticmethod
    def categories_choice(db):
        print('\nVeuillez d\'abord choisir une catégorie d\'aliments :\n')

        index, limit = 0, 28

        for category in db.json_categories['tags']:
            print(index + 1, '. ', category['name'], sep='')
            index += 1

            if index == limit:
                break

        print('\nEntrez un numéro, puis appuyez sur \'Entrée\' :')

    def category_list(self, cat_choice):
        self.cursor.execute('SELECT pur_beurre_catégories_produits.numéro_produit, pur_beurre_produits.nom_aliment FROM pur_beurre_catégories_produits '
                            'INNER JOIN pur_beurre_produits ON pur_beurre_catégories_produits.numéro_produit=pur_beurre_produits.numéro_produit '
                            'WHERE numéro_catégorie = {}'.format(cat_choice))
        result = self.cursor.fetchall()
        print('\n', self.cursor.rowcount, ' ', 'résultats :\n', sep = '')

        for rows in result:
            print(rows[0], '. ', rows[1], sep='')

        print('\nEntrez le numéro correspondant à l\'aliment que vous souhaitez consulter, puis appuyez sur \'Entrée\' :')

    def browse_db(self, food_choice):
        self.cursor.execute('SELECT numéro_produit, nom_aliment, note_nutritionnelle, marque, ingrédients, allergènes, magasins, '
                            'labels, lien_OFF FROM pur_beurre_produits WHERE numéro_produit = \'' + str(food_choice) + '\'')
        product_info = self.cursor.fetchone()
        return product_info

    def get_product_category(self, cat_choice):
        self.cursor.execute('SELECT nom_catégorie FROM pur_beurre_catégories WHERE numéro_catégorie = {0}'.format(cat_choice))
        cat = self.cursor.fetchone()
        return cat

    @staticmethod
    def return_result(product_data, cat_choice):
        print('\nNom du produit : {0}'.format(product_data[1]))
        print('Note nutritionnelle (A = meilleure, E = pire) : {0}'.format(product_data[2]))
        print('Catégorie sélectionnée : {0}'.format(cat_choice[0]))
        print('Marque : {0}'.format(product_data[3]))
        print('Liste des ingrédients : {0}'.format(product_data[4]))
        print('Allergènes : {0}'.format(product_data[5]))
        print('Magasins vendant ce produit : {0}'.format(product_data[6]))
        print('Labels qualité du produit : {0}'.format(product_data[7]))
        print('Lien vers la fiche produit sur OpenFoodFacts.org : {0} \n'.format(product_data[8]))

    @staticmethod
    def get_suggestion():
        input('Nous avons trouvé un produit de remplacement qui pourrait vous intéresser, appuyez sur \'Entrée\' pour la consulter :\n')

    def browse_db_suggestion(self, cat_choice):
        self.cursor.execute(
            'SELECT pur_beurre_produits.numéro_produit, pur_beurre_produits.nom_aliment, pur_beurre_produits.note_nutritionnelle, pur_beurre_produits.marque, '
            'pur_beurre_produits.ingrédients, pur_beurre_produits.allergènes, pur_beurre_produits.magasins, pur_beurre_produits.labels, pur_beurre_produits.lien_OFF '
            'FROM pur_beurre_catégories_produits INNER JOIN pur_beurre_produits ON pur_beurre_catégories_produits.numéro_produit=pur_beurre_produits.numéro_produit '
            'WHERE numéro_catégorie = {} ORDER BY note_nutritionnelle'.format(cat_choice))
        product_info = self.cursor.fetchone()
        return product_info

    def store_suggestion(self, product_data):
        choice = input('Souhaitez-vous enregistrer cette suggestion pour pouvoir la consulter ultérieurement ?\n\n'
                       '1. Oui\n2. Non merci, retourner au menu.\n\nEntrez le numéro correspondant à votre choix puis appuyez sur \'Entrée\' :\n')
        if choice is '1':
            insert = 'INSERT INTO pur_beurre_suggestions (id, numéro_produit) VALUES (%s, %s)'
            values = (0, product_data[0])
            input('\nSuggestion enregistrée avec succès ! Appuyez sur \'Entrée\' pour revenir au menu :')
            self.cursor.execute(insert, values)
            self.db.db.commit()
        else:
            pass

    def suggestions_list(self):
        self.cursor.execute('SELECT pur_beurre_suggestions.id, pur_beurre_suggestions.numéro_produit, pur_beurre_produits.nom_aliment FROM pur_beurre_suggestions '
                            'INNER JOIN pur_beurre_produits ON pur_beurre_suggestions.numéro_produit=pur_beurre_produits.numéro_produit')
        result = self.cursor.fetchall()

        if len(result) is 0:
            input('\nDésolé, vous n\'avez pas de suggestions enregistrées.\n\nAppuyez sur \'Entrée\' pour revenir au menu :\n')
            return 0

        else:
            print('')
            for results in result:
                print(results[0], '. ', results[2], sep = '')

    def view_suggestion(self):
        choice = input('\nChoisissez un numéro pour consulter la fiche de l\'aliment correspondant :\n')
        self.cursor.execute(
            'SELECT pur_beurre_suggestions.id, pur_beurre_suggestions.numéro_produit, pur_beurre_produits.nom_aliment, pur_beurre_produits.note_nutritionnelle, pur_beurre_produits.marque, '
            'pur_beurre_produits.ingrédients, pur_beurre_produits.allergènes, pur_beurre_produits.magasins, pur_beurre_produits.labels, pur_beurre_produits.lien_OFF FROM pur_beurre_suggestions '
            'INNER JOIN pur_beurre_produits ON pur_beurre_suggestions.numéro_produit=pur_beurre_produits.numéro_produit WHERE id = \'' + choice + '\'')
        product_info = self.cursor.fetchone()

        print('\nNom du produit : {0}'.format(product_info[2]), sep='')
        print('Note nutritionnelle (A = meilleure, E = pire) : {0}'.format(product_info[3]))
        print('Catégorie sélectionnée : {0}'.format('None'))
        print('Marque : {0}'.format(product_info[4]))
        print('Liste des ingrédients : {0}'.format(product_info[5]))
        print('Allergènes : {0}'.format(product_info[6]))
        print('Magasins vendant ce produit : {0}'.format(product_info[7]))
        print('Labels qualité du produit : {0}'.format(product_info[8]))
        print('Lien vers la fiche produit sur OpenFoodFacts.org : {0} \n'.format(product_info[9]))

        input('Appuyez sur une touche pour revenir au menu :\n')

    @staticmethod
    def incorrect_choice():
        print('\nVotre choix ne fait pas partie de la liste, merci de faire un autre choix.\n')
        input('Appuyez sur une touche pour revenir au menu :\n')

    def run(self):
        self.welcome_text()

        while self.running:
            try:
                self.menu_choice()
                choice = int(input())

                if choice is 1:
                    self.categories_choice(self.db)
                    cat_choice = int(input())

                    if cat_choice > 0:
                        if cat_choice <= self.db.categories_limit:
                            self.category_list(cat_choice)
                            food_choice = int(input())
                            self.return_result(self.browse_db(food_choice), self.get_product_category(cat_choice))

                            self.get_suggestion()
                            self.return_result(self.browse_db_suggestion(cat_choice), self.get_product_category(cat_choice))
                            self.store_suggestion(self.browse_db_suggestion(cat_choice))

                        else:
                            self.incorrect_choice()
                    else:
                        self.incorrect_choice()
                elif choice is 2:
                    if self.suggestions_list() != 0:
                        self.view_suggestion()
                    else:
                        pass

                elif choice is 3:
                    self.running = False

                else:
                    self.incorrect_choice()

            except (ValueError, TypeError):
                self.incorrect_choice()
                continue


if __name__ == "__main__":
    app = App(database)
    database.use()

    app.run()
