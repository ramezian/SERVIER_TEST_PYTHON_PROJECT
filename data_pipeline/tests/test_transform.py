# test_transform.py

import pandas as pd
import pytest
from data_pipeline.modules.transform import (
    find_drug_mentions,
    process_mentions,
    structure_journals_output
)
from data_pipeline.modules.clean import clean_text, normalize_dates_format, cast_id_as_string, fill_in_missing_ids_int

def test_find_drug_mentions():
    # Préparez des DataFrames factices pour les tests
    data = pd.DataFrame({
        "id": [1, 2, 3],
        "title": ["Aspirin for pain relief", "Ibuprofen study", "No drug mentioned"],
        "journal": ["Journal A", "Journal B", "Journal C"]
    })
    drugs = pd.DataFrame({
        "drug": ["Aspirin", "Ibuprofen"]
    })
    
    # Appliquez la fonction de test
    result = find_drug_mentions(data, drugs, "title", source="pubmed")
    
    # Vérifiez les résultats
    assert not result.empty
    assert len(result) == 2
    assert "Aspirin" in result["drug_name"].values
    assert "Ibuprofen" in result["drug_name"].values
    assert (result["source"] == "pubmed").all()

def test_process_mentions():
    # Créez des DataFrames factices pour les tests
    pubmed_csv = pd.DataFrame({
        "id": [1, 2],
        "title": ["Study on Aspirin", "Paracetamol research"],
        "date": ["2020-01-01", "2021-02-02"]
    })
    pubmed_json = pd.DataFrame({
        "id": ["3"],
        "title": ["Ibuprofen analysis"],
        "date": ["2022-03-03"]
    })
    clinical_trials = pd.DataFrame({
        "id": [None, 5],
        "scientific_title": ["Aspirin trial", "Vitamin C test"],
        "date": ["2021-01-01", "2022-02-02"]
    })
    drugs = pd.DataFrame({
        "drug": ["Aspirin", "Ibuprofen"]
    })

    # Appliquez la fonction de test
    result = process_mentions(pubmed_csv, pubmed_json, clinical_trials, drugs)
    
    # Vérifiez la structure de sortie
    assert "journals" in result
    assert len(result["journals"]) > 0
    for journal in result["journals"]:
        assert "title" in journal
        assert "referencedBy" in journal
        assert "pubmedArticles" in journal["referencedBy"]
        assert "clinicalTrials" in journal["referencedBy"]

def test_structure_journals_output():
    # Créez un DataFrame factice pour les tests
    all_mentions = pd.DataFrame({
        "id": [1, 2, 3],
        "title": ["Aspirin article", "Ibuprofen article", "Paracetamol article"],
        "date": ["2020-01-01", "2021-02-02", "2022-03-03"],
        "drug_name": ["Aspirin", "Ibuprofen", "Paracetamol"],
        "source": ["pubmed", "clinical_trials", "pubmed"],
        "journal": ["Journal A", "Journal B", "Journal A"]
    })

    # Appliquez la fonction de test
    result = structure_journals_output(all_mentions)

    # Vérifiez la structure de sortie
    assert "journals" in result
    assert len(result["journals"]) == 2  # Journal A et Journal B

    # Vérifiez le contenu de chaque journal
    journal_a = next(journal for journal in result["journals"] if journal["title"] == "Journal A")
    assert len(journal_a["referencedBy"]["pubmedArticles"]) == 2
    assert len(journal_a["referencedBy"]["clinicalTrials"]) == 0

    journal_b = next(journal for journal in result["journals"] if journal["title"] == "Journal B")
    assert len(journal_b["referencedBy"]["pubmedArticles"]) == 0
    assert len(journal_b["referencedBy"]["clinicalTrials"]) == 1
