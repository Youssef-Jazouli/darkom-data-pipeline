import pandas as pd
from sqlalchemy import text
from config import engine

def load_to_warehouse(df):
    print("🏗️ Étape 3: Chargement dans le Data Warehouse (Star Schema)...")
    
    # Création du schéma BI et Drop des anciennes tables
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS bi_schema;"))
        conn.execute(text("DROP TABLE IF EXISTS bi_schema.fact_annonces CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS bi_schema.dim_lieu CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS bi_schema.dim_bien CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS bi_schema.dim_temps CASCADE;"))

    # 1. Dimension Lieu
    df_lieu = df[['ville', 'quartier']].drop_duplicates().reset_index(drop=True)
    df_lieu.insert(0, 'lieu_id', df_lieu.index + 1)
    df_lieu.to_sql('dim_lieu', engine, schema='bi_schema', if_exists='replace', index=False)
    
    # 2. Dimension Bien
    cols_bien = ['type_bien', 'transaction', 'nb_chambres', 'nb_salles_bain', 'etage', 'annee_construction', 'categorie_surface']
    df_bien = df[cols_bien].drop_duplicates().reset_index(drop=True)
    df_bien.insert(0, 'bien_id', df_bien.index + 1)
    df_bien.to_sql('dim_bien', engine, schema='bi_schema', if_exists='replace', index=False)
    
    # 3. Dimension Temps
    cols_temps = ['date_publication', 'annee_pub', 'mois_pub', 'trimestre_pub']
    df_temps = df[cols_temps].drop_duplicates().reset_index(drop=True)
    df_temps.to_sql('dim_temps', engine, schema='bi_schema', if_exists='replace', index=False)
    
    # 4. Table de Faits + Sécurité anti-doublons après Merge
    df_merged = df.merge(df_lieu, on=['ville', 'quartier'], how='left').merge(df_bien, on=cols_bien, how='left')
    df_fact = df_merged[['annonce_id', 'lieu_id', 'bien_id', 'date_publication', 'prix', 'surface', 'prix_m2', 'categorie_prix']]
    
    # Sécurisation finale des IDs uniques pour la Primary Key
    df_fact = df_fact.drop_duplicates(subset=["annonce_id"], keep="first")
    df_fact.to_sql('fact_annonces', engine, schema='bi_schema', if_exists='replace', index=False)


def optimize_and_validate():
    print("🔑 Étape 4: Application des clés primaires et étrangères...")
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