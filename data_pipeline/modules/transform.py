import pandas as pd
from typing import Dict
from .clean import clean_text, fill_in_missing_ids_int
from .clean import normalize_dates_format, cast_id_as_string, fill_in_missing_ids_int, clean_text

def find_drug_mentions(data: pd.DataFrame, drugs: pd.DataFrame, title_column: str, source: str) -> pd.DataFrame:
    mentions = []
    for _, drug_row in drugs.iterrows():
        drug_name = drug_row['drug']  # Utilisez uniquement la colonne contenant le nom du médicament
        matches = data[data[title_column].str.contains(drug_name, case=False, na=False)].copy()
        if not matches.empty:
            matches['drug_name'] = drug_name
            matches['source'] = source
            matches['journal'] = matches['journal'].apply(clean_text)
            mentions.append(matches)
    return pd.concat(mentions) if mentions else pd.DataFrame()

def process_mentions(pubmed_csv: pd.DataFrame, pubmed_json: pd.DataFrame, clinical_trials: pd.DataFrame, drugs: pd.DataFrame) -> Dict:
    """
    Traite les données pour extraire les mentions de médicaments et structure les données de sortie.
    """
    # Normaliser les dates et IDs
    pubmed_csv = normalize_dates_format(pubmed_csv, "date")
    pubmed_csv = cast_id_as_string(pubmed_csv, "id")
    pubmed_json = normalize_dates_format(pubmed_json, "date")
    pubmed_json = cast_id_as_string(pubmed_json, "id")
    clinical_trials = normalize_dates_format(clinical_trials, "date")
    clinical_trials = fill_in_missing_ids_int(clinical_trials, "id")

    # Trouver les mentions de médicaments
    pubmed_mentions = find_drug_mentions(pubmed_csv, drugs, 'title', source='pubmed')
    clinical_mentions = find_drug_mentions(clinical_trials, drugs, 'scientific_title', source='clinical_trials')

    # Fusionner les résultats
    all_mentions = pd.concat([pubmed_mentions, clinical_mentions], ignore_index=True)

    return structure_journals_output(all_mentions)

def structure_journals_output(all_mentions: pd.DataFrame) -> dict:
    journals_output = {"journals": []}
    for journal, group in all_mentions.groupby("journal"):
        pubmed_articles = []
        clinical_trials = []
        
        for _, row in group.iterrows():
            entry = {
                "articleId": row['id'],  # Remplacez 'drug_id' par 'id' ou tout autre identifiant approprié
                "articleTitle": row['title'],
                "mentionDate": row['date'],
                "mentionedDrugName": row['drug_name']
            }
            
            # Ajouter l'entrée à la liste appropriée
            if row['source'] == 'pubmed':
                pubmed_articles.append(entry)
            else:
                clinical_trials.append(entry)
        
        journals_output["journals"].append({
            "title": journal,
            "referencedBy": {
                "pubmedArticles": pubmed_articles,
                "clinicalTrials": clinical_trials
            }
        })
    
    return journals_output
