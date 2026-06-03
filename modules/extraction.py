import pandas as pd
from config import engine, CSV_PATH

def extract_to_staging():
    print("⏳ Étape 1: Extraction des données vers le Staging...")
    
    # Charge le fichier CSV et convertit toutes les colonnes en texte (string) pour éviter les erreurs de format
    df = pd.read_csv(CSV_PATH).astype(str)
    
    # Envoie les données brutes directement dans la table 'annonces_brutes' du dossier 'staging'
    df.to_sql('annonces_brutes', engine, schema='staging', if_exists='replace', index=False)
    
    return df