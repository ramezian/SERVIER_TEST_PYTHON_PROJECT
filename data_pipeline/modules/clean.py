# clean.py
import pandas as pd
import re
from typing import List, Dict
from pandera.typing import DataFrame

def normalize_dates_format(df: DataFrame, date_column_name: str, output_date_format: str = "%d/%m/%Y") -> DataFrame:
    """
    Standardizes the date format in the specified DataFrame column to the given output date format.
    """
    df[date_column_name] = pd.to_datetime(df[date_column_name], errors='coerce', dayfirst=True)
    df[date_column_name] = df[date_column_name].dt.strftime(output_date_format).fillna("None")
    return df

def cast_id_as_string(df: pd.DataFrame, id_column_name: str) -> pd.DataFrame:
    """
    Cast the specified column in the DataFrame as a string type, handling NaN and empty values.
    """
    df[id_column_name] = df[id_column_name].apply(lambda x: str(int(x)) if pd.notna(x) else 'nan')
    return df

def rename_column(df: DataFrame, column_naming_mapping: Dict) -> DataFrame:
    """
    Rename one or multiple columns in a DataFrame.
    """
    return df.rename(columns=column_naming_mapping)

def fill_in_missing_ids_int(df: DataFrame, id_column_name: str) -> DataFrame:
    """
    Fills missing integer IDs sequentially, ensuring no gaps in the ID sequence.
    """
    df[id_column_name] = pd.to_numeric(df[id_column_name], errors="coerce")
    max_id = int(df[id_column_name].max()) if pd.notna(df[id_column_name].max()) else 0
    missing_ids = list(range(1, max_id + 1))
    current_ids = df[id_column_name].dropna().unique().tolist()
    ids_to_fill = [i for i in missing_ids if i not in current_ids]
    df.loc[df[id_column_name].isna(), id_column_name] = ids_to_fill
    df[id_column_name] = df[id_column_name].astype(int)
    return df

def clean_titles(current_title: str) -> str:
    """
    Cleans titles by removing special characters, normalizing text, and handling non-ASCII characters.
    """
    if isinstance(current_title, str):
        current_title = re.sub(r"\\x[0-9a-fA-F]{2}", "", current_title)
        current_title = re.sub(r"[^\w\s&ÀàÀ-ÿ-]", "", current_title)
        current_title = re.sub(r"&", "and", current_title)
        current_title = current_title.title().strip()
    return current_title

def clean_text(text: str) -> str:
    """
    Cleans text by removing non-ASCII characters, special punctuation, and normalizing content.
    """
    if isinstance(text, str):
        text = re.sub(r'[^\x20-\x7E]+', '', text)
        text = re.sub(r'\\x[0-9A-Fa-f]{2}', '', text)
        text = re.sub(r'[\(\)]', '', text)
        text = re.sub(r'&', 'and', text)
        text = re.sub(r'\s+', ' ', text)
    return text.strip()

def drop_empty_titles_and_journals(df: DataFrame) -> DataFrame:
    """
    Drops rows where either 'title' or 'journal' column is empty.
    """
    filter_condition = (
        (df["title"] != "")
        & (pd.notna(df["title"]))
        & (df["journal"] != "")
        & (pd.notna(df["journal"]))
    )
    filtered_df = df[filter_condition]
    return filtered_df

def drop_duplicate_ids_then_index(
    drugs_df: DataFrame, all_articles_df: DataFrame
) -> List[DataFrame]:
    """
    Drop duplicate IDs from the DataFrames, then index them using the ID column.
    """
    drugs_df = drugs_df.drop_duplicates(subset=["atccode"], keep="first").reset_index(drop=True)
    all_articles_df = all_articles_df.drop_duplicates(subset=["id"], keep="first").reset_index(drop=True)

    if "atccode" in drugs_df.columns:
        drugs_df.set_index("atccode", inplace=True)
    if "id" in all_articles_df.columns:
        all_articles_df.set_index("id", inplace=True)

    return [drugs_df, all_articles_df]
