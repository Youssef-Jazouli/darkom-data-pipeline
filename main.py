import time
from modules.extraction import extract_to_staging
from modules.transformation import transform_and_clean
from modules.loading import init_schemas, load_to_warehouse, optimize_and_validate, cleanup_staging

if __name__ == "__main__":
    start_time = time.time()
    print("🚀 DÉMARRAGE DU PIPELINE DARKOM...")
    
    # 1. Initialisation des schémas
    init_schemas()
    
    # 2. Extraction
    extract_to_staging()
    
    # 3. Transformation et Nettoyage
    cleaned_df = transform_and_clean()
    
    # 4. Chargement dans le Data Warehouse
    load_to_warehouse(cleaned_df)
    
    # 5. Optimisation (Création des relations)
    optimize_and_validate()  
    
    # 6. Libération de l'espace
    cleanup_staging()
    
    end_time = time.time()
    print(f"🎉 PIPELINE TERMINÉ AVEC SUCCÈS EN {round(end_time - start_time, 2)} SECONDES !")