PUR BEURRE - OPC

A l'ouverture du programme, affichage de 2 choix :

1. Spécifier un aliment à remplacer
2. Voir mes suggestions de remplacement précédentes

Si première visite et choix = 2, afficher "vous n'avez pas encore spécifié d'aliment à remplacer"
-> retour au menu

Si choix = 1, afficher liste de catégories d'aliments, et demander de choisir le numéro correspondant.
=> DONC IMPORTER UNE LISTE DE CATEGORIE D'ALIMENTS

Si choix != numéro valide, afficher "votre choix ne fait pas partie de la liste, merci de faire un autre choix".

Si choix == numéro valide, afficher : "vous avez choisi " aliment_choisi "voila un aliment du même genre qui pourrait avantageusement remplacer votre choix :"
> aliment_suggéré + description + magasin où acheter (si existant) + lien vers page OFF
DONC POUR CHAQUE CATEGORIE D'ALIMENTS, IMPORTER UNE LISTE D'ALIMENTS CORRESPONDANTS3

> Pour enregistrer cette suggestion dans votre base de données, appuyez sur 'E', sinon appuyez sur 'Entrée'

Si choix == Entrée, revenir au menu
Si choix == E, l'ajouter à la base de donnée propre à l'utilisateur sous le format:
> Numéro, Aliment choisi = aliment_choisi, Aliment de remplacement suggéré = aliment_suggéré
> Appuyez sur un numéro pour ouvrir les détails de l'aliment choisi
> Ou appuyez sur Entrée pour revenir au menu



CREATE TABLE pur_beurre_table (id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT, nom_aliment VARCHAR(64) NOT NULL, catégories VARCHAR(128) NULL, marques VARCHAR(64) NULL, ingrédients TEXT NULL, additifs TEXT NULL, allergènes TEXT NULL, notes_nutritionnelles VARCHAR(32) NULL, magasins VARCHAR(128) NULL, labels VARCHAR(128) NULL, lien_OFF VARCHAR(128) NOT NULL, PRIMARY KEY (id));
id, nom_aliment, catégories, marques, ingrédients, additifs, allergènes, notes_nutritionnelles, magasin, labels, lien OFF

INSERT INTO pur_beurre_table VALUES (NULL, "pomme", "fruit", "apple", "sucre", "e100", "vers", "A", "apple store", "qsd.com");

INSERT INTO pur_beurre_table (id, nom_aliment, catégories, marques, ingrédients, additifs, allergènes, notes_nutritionnelles, magasin, lien OFF) VALUES (NULL, "pomme", "fruit", "apple", "sucre", "e100", "vers", "A", "apple store", "qsd.com");