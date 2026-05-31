# Darkom Data Pipeline 🏠📊

A complete ETL (Extract, Transform, Load) data pipeline for Moroccan real estate announcements, designed to build a scalable data warehouse with Power BI integration.

## 📋 Project Overview

This project processes raw real estate listing data and transforms it into a structured data warehouse using a **Star Schema** model. The pipeline includes:

- **Data Extraction**: Raw CSV data loaded into staging
- **Data Transformation**: Cleaning, validation, and feature engineering
- **Data Warehouse**: Star schema with dimensions and fact tables
- **Business Intelligence**: Power BI dashboard integration

## 🏗️ Architecture

### Database Schema Layers

```
├── Staging Schema (staging)
│   └── annonces_brutes - Raw data from CSV
├── Clean Schema (clean)
│   └── annonces_propres - Cleaned and processed data
└── Data Warehouse Schema (bi_schema)
    ├── dim_lieu (Location Dimension)
    ├── dim_bien (Property Dimension)
    ├── dim_temps (Time Dimension)
    └── fact_annonces (Fact Table)
```

### Star Schema Design

**Dimensions:**
- **dim_lieu**: Location details (City, District)
- **dim_bien**: Property characteristics (Type, Rooms, Bathrooms, Construction Year, etc.)
- **dim_temps**: Time information (Publication Date, Year, Month, Quarter)

**Fact Table:**
- **fact_annonces**: Central facts with keys to dimensions and metrics (Price, Surface, Price/m², Category)

## 🚀 Pipeline Stages

### 1. **Extraction**
- Reads raw CSV file using Pandas
- Loads all data as text to preserve original state
- Stores in `staging.annonces_brutes` table

### 2. **Transformation & Cleaning**
Performs comprehensive data quality operations:

**Type Corrections:**
- Converts price and surface to numeric
- Standardizes dates and text fields
- Handles missing values intelligently

**Data Validation:**
- Removes duplicates by announcement ID
- Filters logical errors (price > 100, surface > 9 m²)
- Cleans whitespace and standardizes text casing

**Feature Engineering:**
- `prix_m2`: Price per square meter
- `age_bien`: Property age (2026 - construction year)
- `categorie_prix`: Price categorization (Éco/Moyen/Haut/Luxe)
- `categorie_surface`: Size categorization (Petit/Moyen/Grand)
- Extracts temporal features (year, month, quarter of publication)

Stores cleaned data in `clean.annonces_propres` table

### 3. **Loading to Data Warehouse**
Creates dimensions and fact tables:
- Builds dimension tables with unique values
- Assigns surrogate keys (lieu_id, bien_id)
- Creates fact table with foreign key relationships

### 4. **Optimization & Validation**
- Adds primary keys to all tables
- Creates foreign key constraints for referential integrity
- Ensures data relationships for automatic Power BI linking

### 5. **Cleanup**
- Removes staging data to free space
- Maintains clean production schema

## 📊 Data Model

| Field | Type | Description |
|-------|------|-------------|
| annonce_id | String | Unique announcement identifier |
| prix | Numeric | Property price (MAD) |
| surface | Numeric | Total surface area (m²) |
| ville | String | City name |
| quartier | String | District/Neighborhood |
| type_bien | String | Property type (Apartment, Villa, etc.) |
| transaction | String | Transaction type (Sale, Rent) |
| nb_chambres | Integer | Number of bedrooms |
| nb_salles_bain | Integer | Number of bathrooms |
| etage | Integer | Floor number |
| annee_construction | Integer | Construction year |
| date_publication | Date | Announcement publication date |
| prix_m2 | Numeric | Price per square meter |
| age_bien | Integer | Property age in years |
| categorie_prix | String | Price tier (Éco/Moyen/Haut/Luxe) |
| categorie_surface | String | Size tier (Petit/Moyen/Grand) |

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL database
- pandas, sqlalchemy, psycopg2-binary

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database Connection
Edit `config.py` with your PostgreSQL credentials:
```python
DB_USER = "your_username"
DB_PASS = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Darkom-Data-Pipeline"
```

### 3. Prepare Data
Place your CSV file at: `data/raw/darkom-annonces.csv`

Expected columns:
- annonce_id, prix, surface, ville, quartier, type_bien, transaction, nb_chambres, nb_salles_bain, etage, annee_construction, date_publication

### 4. Run Pipeline
```bash
python main.py
```

Expected output:
```
🚀 DÉMARRAGE DU PIPELINE DARKOM...
⏳ Étape 1: Extraction des données vers le Staging...
🧹 Étape 2: Nettoyage et Feature Engineering...
🏗️ Étape 3: Chargement dans le Data Warehouse...
🔑 Étape 4: Application des clés primaires et étrangères...
🎉 PIPELINE TERMINÉ AVEC SUCCÈS EN X.XX SECONDES !
```

## 📁 Project Structure

```
darkom-data-pipeline/
├── main.py                          # Pipeline orchestration
├── config.py                        # Database configuration
├── requirements.txt                 # Python dependencies
├── modules/
│   ├── __init__.py
│   ├── extraction.py               # Data extraction logic
│   ├── transformation.py           # Data cleaning & feature engineering
│   ├── loading.py                  # Data warehouse loading
│   └── test.ipynb                  # Jupyter notebook for testing
├── data/
│   └── raw/
│       └── darkom-annonces.csv     # Source data
├── dashboards/
│   └── darkom.pbix                 # Power BI dashboard
└── README.MD                        # Documentation
```

## 📈 Power BI Integration

The Star Schema is optimized for Power BI:
- Direct table relationships via foreign keys
- Automatic relationship detection
- Ready for dimensional analysis
- Supports slicing by location, property type, and time period

Use `dashboards/darkom.pbix` to visualize the data warehouse.

## 🔍 Key Features

✅ **Robust Data Cleaning** - Handles missing values, duplicates, and outliers  
✅ **Feature Engineering** - Creates meaningful derived features  
✅ **Star Schema** - Optimized for OLAP analysis and BI tools  
✅ **Data Validation** - Ensures referential integrity  
✅ **Modular Design** - Separable extraction, transformation, and loading steps  
✅ **Error Handling** - Coercive data type conversion with fallbacks  

## 📝 Code Comments

The code includes French comments explaining key concepts, ideal for presentation to stakeholders or instructors:

- "À dire au prof" sections highlight main ideas to communicate
- Data flow is clearly documented
- Business logic is explicit

## 🚦 Error Handling

The pipeline uses pandas `.coerce` error handling:
- **Invalid prices/surfaces** → NaN, filtered out
- **Invalid dates** → Default to 2026-01-01
- **Missing categorical data** → Default values (0 for numbers, "Inconnu" for text)
- **Duplicates** → Removed based on announcement ID

## 💡 Future Enhancements

- [ ] Incremental loading (only new/updated records)
- [ ] Data quality monitoring and logging
- [ ] Automated scheduling (Airflow/Cron)
- [ ] Real-time data pipeline for live announcements
- [ ] Machine learning models for price prediction
- [ ] API layer for data access

## 📌 Notes

- All prices are in Moroccan Dirhams (MAD)
- Data is Moroccan real estate focused
- Pipeline defaults to 2026 as current year for age calculations
- Minimum viable property size: 9 m²
- Minimum viable price: 100 MAD

## 📞 Support

For issues or questions about the pipeline, review:
1. Database connection settings in `config.py`
2. Input CSV format matches expected columns
3. PostgreSQL database is running and accessible
4. Required Python packages are installed

---

**Status**: ✅ Production Ready  
**Last Updated**: 2026  
**Language**: Python 3 + SQL
