import pandas as pd
from config import engine, CSV_PATH
from sqlalchemy import text

def extract_to_staging():
    print("⏳ Étape 1: Extraction des données vers le Staging...")
    
    # Création du schéma staging s'il n'existe pas
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging;"))
        conn.commit()

    # Charge le fichier CSV et convertit toutes les colonnes en texte
    df = pd.read_csv(CSV_PATH).astype(str)
    
    # Envoie les données brutes directement dans la table 'annonces_brutes'
    df.to_sql('annonces_brutes', engine, schema='staging', if_exists='replace', index=False)
    
    return df