import pandas as pd
from config import engine, CSV_PATH

def extract_to_staging():
    """À dire au prof: Extraction avec Pandas. Les données sont chargées en format texte dans Staging pour conserver l'état brut."""
    print("⏳ Étape 1: Extraction des données vers le Staging...")
    df = pd.read_csv(CSV_PATH).astype(str)
    df.to_sql('annonces_brutes', engine, schema='staging', if_exists='replace', index=False)
    return df