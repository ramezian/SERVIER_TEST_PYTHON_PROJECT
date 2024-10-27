

import json

def save_json(data, filepath):
    """
    Enregistre les données sous forme de fichier JSON.

    Paramètres :
        - data : Les données à sauvegarder.
        - filepath : Le chemin où sauvegarder le fichier JSON.
    """
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)