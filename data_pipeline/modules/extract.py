import pandas as pd
import yaml
import os

def load_config(config_file="config/config.yaml"):
    """Charge le fichier de configuration YAML."""
    with open(config_file, "r") as file:
        return yaml.safe_load(file)

#def load_config():
#    # Utiliser un chemin absolu pour le fichier config.yaml
#    config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/config.yaml"))
#    
#    with open(config_file, "r") as file:
#        config = yaml.safe_load(file)
#    
#    return config


##def load_config():
##    # Chemin absolu direct vers config.yaml
##    config_file = "/home/ridou/Servier_pyhton_projet/etl/data_pipeline/config/config.yaml"  
##    
##    with open(config_file, "r") as file:
##        config = yaml.safe_load(file)
##    
##    return config

def extract_csv(file_path: str) -> pd.DataFrame:
    """Lire les données d'un fichier CSV et les retourner sous forme de DataFrame."""
    return pd.read_csv(file_path)

def extract_json(file_path: str) -> pd.DataFrame:
    """Lire les données d'un fichier JSON et les retourner sous forme de DataFrame."""
    return pd.read_json(file_path)
