"""
Programme réalisé dans le cadre d'un exercice Python CLI
Il prend en entrée une requête à base de mots clés et,à partir de l'API EHR Portal,
sort un fichier CSV (?) contenant les données qui y sont associées.
"""

import requests, json

# Création du programme de base avant transformation en CLI
# Requetage JSon: récupération de l'url puis des données associées pour le cas de documentaryunit

def documentaryUnitrecup(mot_cle):
    url = "https://portal.ehri-project.eu/api/v1/search?type="+mot_cle
    requete = requests.get(url)
    donnees = requete.json()
    for objet in donnees['data']:
        #exemple de données à récupérer, à voir lesquelles prendre
        id=objet['id']
        type=objet['type']
        nom=objet['attributes']['descriptions'][0]['name']
        lien=objet['links']['self']
        #pour l'instant uniquement affichage des donnés obtenues, à mettre sous forme csv après?
        print(id, type, nom, lien)

recherche_utilisateur=input('Rentrez un mot clé (Documentary Unit):')
documentaryUnitrecup(recherche_utilisateur)