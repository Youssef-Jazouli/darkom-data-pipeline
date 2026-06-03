import pandas as pd
from sqlalchemy import text
from config import engine

def load_to_warehouse(df):
    print("🏗️ Étape 3: Chargement dans le Data Warehouse (Star Schema)...")
    
    # NETTOYAGE RADICAL: Force le DROP de la table de faits et ses contraintes avant tout chargement
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS bi_schema.fact_annonces CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS bi_schema.dim_lieu CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS bi_schema.dim_bien CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS bi_schema.dim_temps CASCADE;"))

    # 1. Création de la Dimension Lieu
    df_lieu = df[['ville', 'quartier']].drop_duplicates().reset_index(drop=True)
    df_lieu.insert(0, 'lieu_id', df_lieu.index + 1)
    df_lieu.to_sql('dim_lieu', engine, schema='bi_schema', if_exists='replace', index=False)
    
    # 2. Création de la Dimension Bien
    cols_bien = ['type_bien', 'transaction', 'nb_chambres', 'nb_salles_bain', 'etage', 'annee_construction', 'age_bien', 'categorie_surface']
    df_bien = df[cols_bien].drop_duplicates().reset_index(drop=True)
    df_bien.insert(0, 'bien_id', df_bien.index + 1)
    df_bien.to_sql('dim_bien', engine, schema='bi_schema', if_exists='replace', index=False)
    
    # 3. Création de la Dimension Temps
    cols_temps = ['date_publication', 'annee_pub', 'mois_pub', 'trimestre_pub']
    df_temps = df[cols_temps].drop_duplicates().reset_index(drop=True)
    df_temps.to_sql('dim_temps', engine, schema='bi_schema', if_exists='replace', index=False)
    
    # 4. Création de la Table de Faits (Fact Table)
    df_merged = df.merge(df_lieu, on=['ville', 'quartier'], how='left').merge(df_bien, on=cols_bien, how='left')
    df_fact = df_merged[['annonce_id', 'lieu_id', 'bien_id', 'date_publication', 'prix', 'surface', 'prix_m2', 'categorie_prix']]
    df_fact.to_sql('fact_annonces', engine, schema='bi_schema', if_exists='replace', index=False)


def optimize_and_validate():
    print("🔑 Étape 4: Application des clés primaires et étrangères...")
    # SQL pour lier les tables bيناتهم b les Primary Keys w les Foreign Keys
    queries = [
        "ALTER TABLE bi_schema.dim_lieu ADD PRIMARY KEY (lieu_id);",
        "ALTER TABLE bi_schema.dim_bien ADD PRIMARY KEY (bien_id);",
        "ALTER TABLE bi_schema.dim_temps ADD PRIMARY KEY (date_publication);",
        "ALTER TABLE bi_schema.fact_annonces ADD PRIMARY KEY (annonce_id);",
        "ALTER TABLE bi_schema.fact_annonces ADD CONSTRAINT fk_l FOREIGN KEY (lieu_id) REFERENCES bi_schema.dim_lieu(lieu_id);",
        "ALTER TABLE bi_schema.fact_annonces ADD CONSTRAINT fk_b FOREIGN KEY (bien_id) REFERENCES bi_schema.dim_bien(bien_id);",
        "ALTER TABLE bi_schema.fact_annonces ADD CONSTRAINT fk_t FOREIGN KEY (date_publication) REFERENCES bi_schema.dim_temps(date_publication);"
    ]
    with engine.begin() as conn:
        for q in queries: 
            conn.execute(text(q))