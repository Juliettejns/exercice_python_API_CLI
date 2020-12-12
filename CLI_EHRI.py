import requests, json, click


# Création du programme de base avant transformation en CLI
# Requetage JSon: récupération de l'url puis des données associées.
# Pour l'instant j'ai uniquement travaillé sur un mot clé correspondant au type mais je pense qu'on peut tenter d'
# ajouter un deuxième argument, par exemple ne faire ressortir que les objets où l'on retrouve ce 2ème argument?

@click.command()
@click.argument("mot_cle", type=str)
def requetage(mot_cle):
    """Exécute une recherche sur l'API EHRI à partir de l'entrée d'un mot-clé issu de cette liste restreinte:
    Country, Repository, HistoricalAgent, DocumentaryUnit.
    :param mot_cle: chaîne de caractères rentrée par l'utilisateur.
    :type mot_cle: str
    :param resultat: liste de liste contenant les données importantes de la requête
    :type resultat: list
    """

    url = "https://portal.ehri-project.eu/api/v1/search?type=" + mot_cle
    requete = requests.get(url)
    donnees = requete.json()
    resultat = []
    for objet in donnees['data']:
        try:
            # exemple de données à récupérer, à voir lesquelles prendre
            id_objet = objet['id']
            type_objet = objet['type']
            description = objet["attributes"]["descriptions"][0]
            nom = description["name"]
            presentation = description["scopeAndContent"]
            lien = objet['links']['self']

            resultat.append([id_objet, type_objet, nom, presentation, lien])
        # fonctionne mais uniquement pour le mot-clé DocumentaryUnit car structure des données diffère selon mot-clé
        except (IndexError, KeyError):
            pass
    print(resultat)


if __name__ == "__main__":
    requetage()
