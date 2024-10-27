# test_extract.py

import pytest
from data_pipeline.modules.extract import extract_csv, extract_json, load_config
import os

def test_extract_csv():
    # Test de l'extraction d'un fichier CSV
    df = extract_csv('data/drugs.csv')
    assert df is not None, "DataFrame should not be None"
    assert not df.empty, "DataFrame should not be empty"

def test_extract_json():
    # Test de l'extraction d'un fichier JSON
    df = extract_json('data/pubmed.json')
    assert df is not None, "DataFrame should not be None"
    assert not df.empty, "DataFrame should not be empty"

def test_load_config():
    # Test du chargement du fichier de configuration
    config = load_config('config/config.yaml')
    assert 'data_paths' in config, "'data_paths' should be in config"
    assert 'output_path' in config, "'output_path' should be in config"
