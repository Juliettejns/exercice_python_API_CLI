
@click.group()
def interrogation_EHRI():
    """Ensemble de commandes pour interroger l'API EHRI"""
    return=True


@interrogation_EHRI.command("requetage")
@click.argument("query", type=str)
def requetage(query):

    """Exécute une recherche sur l'API EHRI à partir de l'entrée d'un mot-clé issu de cette liste restreinte: Country, Repository, HistoricalAgent, DocumentaryUnit."""

"""def requetage(q):
    Fait une recherche sur l'API EHRI à partir de l'entrée d'un mot-clé issu de cette liste restreinte:
    Country, Repository, HistoricalAgent, DocumentaryUnit.
    :param mot_cle: chaîne de caractères rentrée par l'utilisateur.
    :type mot_cle: str
    :param resultat: liste de liste contenant les résultats de la requête
    :type resultat: list
     """

    parametres={"q":q}
    url = "https://portal.ehri-project.eu/api/v1/search?"
    requete = requests.get(url, params=parametres)
    donnees = requete.json()
    resultat=[]
    for objet in donnees['data']:

        try:
        #Récupération des valeurs des clés qui nous importent pour le requêtage des données principales de présentation et de description.
            resultat.append({"id": objet['id'],
                            "type": objet['type'],
                            "lien": objet['links']['self'],
                            "nom":[]
                             })
        #L'hétérogénéité de la structure des données selon le mot-clé impose l'usage d'une condition.
            if objet['type']=="Repository" or objet['type']=="HistoricalAgent":
                resultat[-1]['nom'].append(objet['attributes']['name'])
            elif objet['type']=="DocumentaryUnit":
                description = objet["attributes"]["descriptions"][0]
                resultat[-1]['nom'].append(description["name"])
        except (IndexError, KeyError):
            pass
        #En cas d'absence de valeurs pour les clés recherchées, ou d'absence de clé, le programme se poursuit malgré tout.
    print(resultat)


if __name__ == "__main__":
    requetage()


@interrogation_EHRI.command('requetage_historique')
@click.argument('nom_unite_documentaire')
#Permet d'afficher uniquement les présentations des unités documentaires en langue allemande.
def requetage_historique(nom_unite_documentaire):
    parametres={"q":q}
    url = "https://portal.ehri-project.eu/api/v1/search?"
    requete = requests.get(url, params=parametres)
    donnees = requete.json()
    resultat=[]
    for objet in donnees['data']:
        description = objet["attributes"]["descriptions"][0]
        presentation=description['scopeAndContent']
        if ['type']=="DocumentaryUnit" and description['language'] == "allemand":
            print(presentation)

if __name__ == "__main__":
    requetage_historique()


@interrogation_EHRI.command('run')
@click.argument("query", type=str)
@click.option("-f", "--full", is_flag=True, default=False, help="obtenir toutes les informations récupérées")
def run(query, full):
    """Exécute une recherche sur API EHRI et l'affiche dans le terminal"""
    resultat=requetage(query)
    print("Nombre de résultats:{}".format(len(resultat)))

    for objet in resultat:
        print("nom:{}, type:{}".format(objet['nom'], objet['type']))
    if full:
        for objet in resultat:
            print("id: {}, nom:{}, type:{}, lien:{}".format(objet['id'], objet['nom'], objet['type'], objet['lien']))


if __name__ == "__main__":
   run()