# test_clean.py

import pandas as pd
import pytest
from data_pipeline.modules.clean import (
    normalize_dates_format,
    clean_text,
    cast_id_as_string,
    rename_column,
    fill_in_missing_ids_int,
    clean_titles,
    drop_empty_titles_and_journals,
    drop_duplicate_ids_then_index
)

def test_normalize_dates_format():
    # Utilise des dates variées pour tester la conversion
    df = pd.DataFrame({"date": ["12 Janvier 2020", "13/02/2021", "2022-03-14", None]})
    df = normalize_dates_format(df, "date", "%d/%m/%Y")
    expected_dates = ["12/01/2020", "13/02/2021", "14/03/2022", None]
    assert df["date"].fillna("None").tolist() == [str(d) if d is not None else "None" for d in expected_dates]

def test_clean_text():
    # Texte avec caractères spéciaux et parenthèses
    text = "This is a sample text with special chars: \xc3\x28 and (parentheses)"
    cleaned_text = clean_text(text)
    assert cleaned_text == "This is a sample text with special chars: and parentheses"

def test_cast_id_as_string():
    # Test pour vérifier la conversion en chaînes de caractères avec gestion des NaN
    df = pd.DataFrame({"id": [1, 2, 3, None]})
    df = cast_id_as_string(df, "id")
    assert df["id"].tolist() == ["1", "2", "3", "nan"]

def test_rename_column():
    # Renommer une colonne et vérifier l'existence et la suppression de l'ancienne colonne
    df = pd.DataFrame({"old_name": [1, 2, 3]})
    df = rename_column(df, {"old_name": "new_name"})
    assert "new_name" in df.columns and "old_name" not in df.columns

def test_fill_in_missing_ids_int():
    # Remplissage d'ID manquants avec une séquence ordonnée
    df = pd.DataFrame({"id": [1, None, 3, None, 5]})
    df = fill_in_missing_ids_int(df, "id")
    assert df["id"].tolist() == [1, 2, 3, 4, 5]

def test_clean_titles():
    # Nettoyage du titre, suppression des caractères spéciaux et normalisation en majuscules
    title = "sample title with \xc3 special & characters (test)"
    cleaned_title = clean_titles(title)
    assert cleaned_title == "Sample Title With Special And Characters Test"

def test_drop_empty_titles_and_journals():
    # Suppression des lignes avec des titres ou journaux vides
    df = pd.DataFrame({
        "title": ["Title 1", "", "Title 3", None],
        "journal": ["Journal 1", "Journal 2", "", None]
    })
    df_cleaned = drop_empty_titles_and_journals(df)
    assert len(df_cleaned) == 1
    assert df_cleaned.iloc[0]["title"] == "Title 1"

def test_drop_duplicate_ids_then_index():
    # Suppression de doublons et test d'indexation
    drugs_df = pd.DataFrame({"atccode": ["A", "B", "A", "C"], "value": [1, 2, 3, 4]})
    articles_df = pd.DataFrame({"id": [1, 2, 2, 3], "title": ["T1", "T2", "T2", "T3"]})

    drugs_df, articles_df = drop_duplicate_ids_then_index(drugs_df, articles_df)
    
    assert len(drugs_df) == 3
    assert len(articles_df) == 3
    assert "A" in drugs_df.index
    assert 1 in articles_df.index
