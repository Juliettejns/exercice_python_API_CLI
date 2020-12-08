"""
Programme réalisé dans le cadre d'un exercice Python CLI
Il prend en entrée une requête à base de mots clés et,à partir de l'API EHR Portal,
sort un fichier CSV (?) contenant les données qui y sont associées.
"""

import requests, json

# Création du programme de base avant transformation en CLI
# Requetage JSon: récupération de l'url puis des données associées.
# Pour l'instant j'ai uniquement travaillé sur un mot clé correspondant au type mais je pense qu'on peut tenter d'
# ajouter un deuxième argument, par exemple ne faire ressortir que les objets où l'on retrouve ce 2ème argument?

def requetage(mot_cle):
    """Récupère les données correspondant à la requête faite par l'utilisateur sur l'API EHRI
     et créé un fichier csv avec celles-ci

    :param mot_cle: chaîne de caractères rentrée par l'utilisateur
    :type mot_cle: str
    :param resultat: liste de liste contenant les données importantes de la requête
    :type resultat: list
     """

    url = "https://portal.ehri-project.eu/api/v1/search?type="+mot_cle
    requete = requests.get(url)
    donnees = requete.json()
    resultat=[]
    for objet in donnees['data']:
        #exemple de données à récupérer, à voir lesquelles prendre
        id=objet['id']
        type=objet['type']
        nom=objet['attributes']['descriptions'][0]['name']
        lien=objet['links']['self']
        #pour l'instant uniquement affichage des donnés obtenues, à mettre sous forme csv après?
        resultat.append([id, type, nom, lien])
    print(resultat)

recherche_utilisateur=input('Rentrez un mot clé (DocumentaryUnit, HistoricalAgent, repository ou country):')
requetage(recherche_utilisateur)