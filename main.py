import pandas as pd
from modules.extraction import extract_to_staging
from modules.transformation import transform_and_clean
from modules.loading import load_to_warehouse, optimize_and_validate

def main():
    print("🚀 DÉMARRAGE DU PIPELINE DARKOM...")
    
    # Étape 1 : Extraction des données brutes depuis le fichier CSV vers le Staging
    raw_df = extract_to_staging()
    
    # Étape 2 : Nettoyage des données et création des nouvelles variables (Feature Engineering)
    cleaned_df = transform_and_clean()
    
    # Étape 3 : Chargement des données dans le Data Warehouse (Modèle en étoile)
    load_to_warehouse(cleaned_df)
    
    # Étape 4 : Configuration des relations (Clés primaires et clés étrangères)
    optimize_and_validate()
    
    print("✅ PIPELINE TERMINÉ AVEC SUCCÈS !")

if __name__ == "__main__":
    main()