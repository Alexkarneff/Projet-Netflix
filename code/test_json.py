import json

infos_utilisateur = {
    "nom": "à saisir ?",
    "nb_connexion": 0, # à incrémenter de 1 à chaque lancement
    "recherches_frequentes" : {} # liste ou dictionnaire regroupant les recherches 
    }

"""
Idée : 
Pour les recherches fréquentes; à chaque fois que l'utilisateur effectue une recherche faire : 
if "recherche" in infos_utilisateur:
    infos_utilisateur["recherche"] += 1
else:
    infos_utilisateur["recherche"] = 1
"""



# Conversion en chaîne JSON
# donnees_json = json.dumps(donnees, indent=4)

# Affichage de la chaîne JSON
# print(donnees_json)