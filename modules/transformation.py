import pandas as pd
import numpy as np
from config import engine

def transform_and_clean():
    print("🧹 Étape 2: Nettoyage et Feature Engineering...")
    # Récupère les données brutes depuis la table de staging
    df = pd.read_sql_table('annonces_brutes', engine, schema='staging')
    
    # 1. Conversion des prix et surfaces + nettoyage des valeurs aberrantes
    df['prix'] = pd.to_numeric(df['prix'], errors='coerce')
    df['surface'] = pd.to_numeric(df['surface'], errors='coerce')
    df = df[(df['prix'] > 100) & (df['surface'] > 9)].drop_duplicates(subset=['annonce_id'])
    
    # 2. Nettoyage et propagation des dates (ffill/bfill)
    df['date_publication'] = pd.to_datetime(df['date_publication'], errors='coerce')
    df['date_publication'] = df['date_publication'].ffill().bfill()
    
    # 3. Nettoyage et propagation du texte (ffill/bfill)
    for col in ['ville', 'quartier', 'type_bien', 'transaction']:
        df[col] = df[col].str.strip().str.title()
        df[col] = df[col].replace('', np.nan).ffill().bfill()
    
    # 4. Nettoyage et propagation des nombres entiers (ffill/bfill)
    for col in ['nb_chambres', 'nb_salles_bain', 'etage', 'annee_construction']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].ffill().bfill().astype(int)
    
    # 5. Feature Engineering (Calculs et nouvelles colonnes)
    df['prix_m2'] = df['prix'] / df['surface']
    df['age_bien'] = 2026 - df['annee_construction']
    
    # Découpage des prix et des surfaces en catégories
    df['categorie_prix'] = pd.cut(df['prix'], bins=[-1, 500000, 1500000, 4000000, np.inf], labels=['Éco', 'Moyen', 'Haut', 'Luxe'])
    df['categorie_surface'] = pd.cut(df['surface'], bins=[-1, 80, 150, np.inf], labels=['Petit', 'Moyen', 'Grand'])
    
    # Extraction des morceaux de la date pour l'analyse temporelle
    df['annee_pub'] = df['date_publication'].dt.year
    df['mois_pub'] = df['date_publication'].dt.month
    df['trimestre_pub'] = df['date_publication'].dt.quarter
    
    # Sauvegarde les données propres dans la table finale du dossier 'clean'
    df.to_sql('annonces_propres', engine, schema='clean', if_exists='replace', index=False)
    return df