from data_pipeline.modules.clean import normalize_dates_format, cast_id_as_string, fill_in_missing_ids_int
from data_pipeline.modules.extract import load_config, extract_csv, extract_json
from data_pipeline.modules.transform import process_mentions, structure_journals_output
from data_pipeline.modules.load import save_json

def main():
    # Charger la configuration
    config = load_config()

    # Extraire les données
    drugs = extract_csv(config["data_paths"]["drugs_csv"])
    pubmed_csv = extract_csv(config["data_paths"]["pubmed_csv"])
    pubmed_json = extract_json(config["data_paths"]["pubmed_json"])
    clinical_trials = extract_csv(config["data_paths"]["clinical_trials_csv"])

    # Préparer et transformer les données
    journals_output = process_mentions(pubmed_csv, pubmed_json, clinical_trials, drugs)

    # Enregistrer les résultats en JSON
    save_json(journals_output, config["output_path"])

    print("Génération du fichier JSON terminée.")

if __name__ == "__main__":
    main()
