import requests, json, click



def requetage(q):
    """Fait une recherche sur l'API EHRI à partir de l'entrée d'un mot-clé issu de cette liste restreinte:
    Country, Repository, HistoricalAgent, DocumentaryUnit.
    :param mot_cle: chaîne de caractères rentrée par l'utilisateur.
    :type mot_cle: str
    :param resultat: liste de liste contenant les données importantes de la requête
    :type resultat: list
    """
    parametres = {"q": q}
    url = "https://portal.ehri-project.eu/api/v1/search?"
    requete = requests.get(url, params=parametres)
    donnees = requete.json()
    resultat = []
    for objet in donnees['data']:

        try:
            # exemple de données à récupérer: ici celles qui fonctionnent pour tout les types de données documentaryUnt...
            # on essaie d'obtenir le nom si il existe, une description si elle existe, les fichiers n'étant pas identiques
            resultat.append({"id": objet['id'],
                             "type": objet['type'],
                             "lien": objet['links']['self'],
                             "nom": [],
                             "langue": []
                             })
            if objet['type'] == "Repository" or objet['type'] == "HistoricalAgent":
                resultat[-1]['nom'].append(objet['attributes']['name'])
            elif objet['type'] == "DocumentaryUnit":
                resultat[-1]['nom'].append(objet['attributes']['descriptions'][0]['name'])
                resultat[-1]['langue'].append(objet['attributes']['descriptions'][0]['language'])
        except (IndexError, KeyError):
            pass
    return resultat


@click.group()
def mon_groupe():
    """Groupe de commandes pour communiquer avec API EHRI"""


@mon_groupe.command("recherche")
@click.argument("query", type=str)
@click.option("-f", "--full", is_flag=True, default=False, help="obtenir toutes les informations récupérées")
@click.option("-s", "--scope", is_flag=True, default=False, help="obtenir toutes les unités archivistiques récupérées")
def run(query, full, scope):
    """Exécute une recherche sur API EHRI et l'affiche dans le terminal"""
    resultat = requetage(query)
    print("Nombre de résultats:{}".format(len(resultat)))

    if full:
        #Affiche toutes les données récupérées
        for objet in resultat:
            print("id: {}, nom:{}, type:{}, lien:{}".format(objet['id'], objet['nom'], objet['type'], objet['lien']))
    elif scope:
        #Affiche toutes les unités documentaires récupérées uniquement.
        n=0
        for objet in resultat:
            if objet['type']=='DocumentaryUnit':
                print("id:{}, nom:{}, langue:{}".format(objet['id'], objet['nom'], objet['langue']))
                n+=1
        print("Il y a {} unités documentaires correspondant à la recherche".format(n))
    else:
        #Affichage de base
        for objet in resultat:
            print("nom:{}, type:{}".format(objet['nom'], objet['type']))


if __name__ == "__main__":
    mon_groupe()
