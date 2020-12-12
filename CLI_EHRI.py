import requests, json, click


# Création du programme de base avant transformation en CLI
# Requetage JSon: récupération de l'url puis des données associées.
# Pour l'instant j'ai uniquement travaillé sur un mot clé correspondant au type mais je pense qu'on peut tenter d'
# ajouter un deuxième argument, par exemple ne faire ressortir que les objets où l'on retrouve ce 2ème argument?



def requetage(mot_cle, full=False):
    """Fait une recherche sur l'API EHRI à partir de l'entrée d'un mot-clé issu de cette liste restreinte:
    Country, Repository, HistoricalAgent, DocumentaryUnit.
    :param mot_cle: chaîne de caractères rentrée par l'utilisateur.
    :type mot_cle: str
    :param resultat: liste de liste contenant les données importantes de la requête
    :type resultat: list
    """

    url = "https://portal.ehri-project.eu/api/v1/search?type=" + mot_cle
    requete = requests.get(url)
    donnees = requete.json()
    resultat=[]
    for objet in donnees['data']:
        try:
            # exemple de données à récupérer: ici celles qui fonctionnent pour tout les mots_clé

            resultat.append({"id": objet['id'],
                             "type": objet['type'],
                             "lien": objet['links']['self']
                             })
        except (IndexError, KeyError):
            pass
    return resultat

@click.command()
@click.argument("query", type=str)
@click.option("-f", "--full", is_flag=True, default=False, help="obtenir toutes les informations récupérées")
def run(query, full):
    """Exécute une recherche sur API EHRI et l'affiche dans le terminal"""
    resultat=requetage(query)
    print("Nombre de résultats:{}".format(len(resultat)))

    for objet in resultat:
        print("id:{}".format(objet['id']))
    if full:
        for objet in resultat:
            print("id{}, type:{}, lien:{}".format(objet['id'], objet['type'], objet['lien']))
if __name__ == "__main__":
   run()
