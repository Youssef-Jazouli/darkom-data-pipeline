import pandas as pd
import numpy as np
from config import engine

def transform_and_clean():
    """À dire au prof: Nettoyage (types, doublons, outliers) et Feature Engineering (prix/m², âge, catégorisation)."""
    print("🧹 Étape 2: Nettoyage et Feature Engineering...")
    df = pd.read_sql_table('annonces_brutes', engine, schema='staging')
    
    # Correction des types et filtres logiques
    df['prix'] = pd.to_numeric(df['prix'], errors='coerce')
    df['surface'] = pd.to_numeric(df['surface'], errors='coerce')
    df = df[(df['prix'] > 100) & (df['surface'] > 9)].drop_duplicates(subset=['annonce_id'])
    
    # Nettoyage des textes et dates
    df['date_publication'] = pd.to_datetime(df['date_publication'], errors='coerce').fillna(pd.to_datetime('2026-01-01'))
    for col in ['ville', 'quartier']: 
        df[col] = df[col].str.strip().str.title().fillna('Inconnu')
    df['type_bien'] = df['type_bien'].str.strip().str.title().fillna('Appartement')
    df['transaction'] = df['transaction'].str.strip().str.title().fillna('Vente')
    
    # Nettoyage des entiers
    for col in ['nb_chambres', 'nb_salles_bain', 'etage', 'annee_construction']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(2020 if col=='annee_construction' else 0).astype(int)
    
    # Feature Engineering
    df['prix_m2'] = df['prix'] / df['surface']
    df['age_bien'] = 2026 - df['annee_construction']
    df['categorie_prix'] = pd.cut(df['prix'], bins=[-1, 500000, 1500000, 4000000, np.inf], labels=['Éco', 'Moyen', 'Haut', 'Luxe'])
    df['categorie_surface'] = pd.cut(df['surface'], bins=[-1, 80, 150, np.inf], labels=['Petit', 'Moyen', 'Grand'])
    df['annee_pub'] = df['date_publication'].dt.year
    df['mois_pub'] = df['date_publication'].dt.month
    df['trimestre_pub'] = df['date_publication'].dt.quarter
    
    df.to_sql('annonces_propres', engine, schema='clean', if_exists='replace', index=False)
    return df