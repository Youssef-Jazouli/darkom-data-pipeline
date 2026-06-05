import os
import logging
import pandas as pd
import numpy as np
from config import engine

def extract_type_bien(title):
    if not isinstance(title, str):
        return None
    title = title.lower()
    if "appartement" in title: return "Appartement"
    elif "villa" in title: return "Villa"
    elif "bureau" in title: return "Bureau"
    elif "terrain" in title: return "Terrain"
    elif "duplex" in title: return "Duplex"
    else: return None

def fill_transaction(row):
    if pd.notna(row["transaction"]) and str(row["transaction"]).strip() != "":
        return row["transaction"]
    if pd.notna(row["prix"]) and row["prix"] <= 30000:
        return "Location"
    else:
        return "Vente"

def transform_and_clean():
    print("🧹 Étape 2: Nettoyage et Feature Engineering...")
    logging.info("🧹 Étape 2: Démarrage du nettoyage et Feature Engineering...")

    query = "SELECT * FROM staging.annonces_brutes"
    df = pd.read_sql(query, engine)

    # ÉTAPE 1 : Nettoyage textuel
    df["ville"] = df["ville"].str.strip().str.title()
    df["quartier"] = df["quartier"].str.strip().str.title()
    df = df.dropna(subset=['ville', 'quartier'])

    # ÉTAPE 2 : Correction des types (Ajout de surface ici)
    df["date_publication"] = pd.to_datetime(df["date_publication"], errors="coerce")
    numeric_columns = ["prix", "surface", "nb_chambres", "nb_salles_bain", "etage", "annee_construction"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ÉTAPE 3 : Gestion des valeurs manquantes
    df = df.sort_values("date_publication").reset_index(drop=True)
    df["date_publication"] = df["date_publication"].ffill().bfill()

    df["quartier"] = df.groupby("ville")["quartier"].transform(
        lambda x: x.fillna(x.mode()[0] if not x.mode().empty else "Unknown")
    )
    df["type_bien"] = df["type_bien"].fillna(df["titre"].apply(extract_type_bien))
    df["transaction"] = df.apply(fill_transaction, axis=1)

    columns_to_fill = ["nb_chambres", "nb_salles_bain", "etage"]
    for col in columns_to_fill:
        df.loc[df["type_bien"] == "Terrain", col] = df.loc[df["type_bien"] == "Terrain", col].fillna(0)
        median_val = df.groupby("type_bien")[col].transform("median")
        df[col] = df[col].fillna(median_val)

    constr_median = df.groupby(["ville", "type_bien"])["annee_construction"].transform("median")
    df["annee_construction"] = df["annee_construction"].fillna(constr_median)

    for col in numeric_columns:
        df[col] = df[col].round().astype("Int64")

    # ÉTAPE 4 : Traitement des Outliers
    df = df[df["surface"] >= 30]
    df = df[df["nb_chambres"] <= 10]
    df = df[df["nb_salles_bain"] <= 6]
    df = df[df["prix"] <= 20000000]

    # ÉTAPE 5 : Feature Engineering
    df['annee_pub'] = df['date_publication'].dt.year.astype("Int64")
    df['mois_pub'] = df['date_publication'].dt.month.astype("Int64")
    df['trimestre_pub'] = df['date_publication'].dt.quarter.astype("Int64")
    df['prix_m2'] = (df['prix'] / df['surface']).round(2)
    df['categorie_surface'] = pd.cut(df['surface'], bins=[0, 50, 100, 150, np.inf], labels=['Petite', 'Moyenne', 'Grande', 'Très Grande'])
    df['categorie_prix'] = pd.cut(df['prix'], bins=[0, 500000, 1000000, 2000000, np.inf], labels=['Économique', 'Standard', 'Haut standing', 'Luxe'])

    # ÉTAPE 6 : Déduplication préventive
    df = df.drop_duplicates(subset=["annonce_id"], keep="first")

    logging.info("✅ STEP 2 END - Nettoyage et Feature Engineering complétés.")
    return df