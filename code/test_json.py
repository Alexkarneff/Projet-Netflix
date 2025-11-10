import json

donnees = {
    "nom": "Stéphane ROBERT",
    "age": 29,
    "adresse": {
        "rue": "456 avenue des Champs",
        "ville": "Lyon",
        "code_postal": "69001"
    },
    "hobbies": ["photographie", "voyage", "musique"]
}

# Conversion en chaîne JSON
donnees_json = json.dumps(donnees, indent=4)

# Affichage de la chaîne JSON
print(donnees_json)