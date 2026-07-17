# 1. Nom du projet

**Nom du projet :** Darkom Data Pipeline

---

# 2. Présentation du projet

Ce projet est une analyse de données et un pipeline ETL automatisé qui permet de collecter, nettoyer et centraliser les annonces immobilières de la plateforme Darkom.ma.

Il s'adresse principalement aux analystes de données, aux investisseurs immobiliers et aux professionnels du secteur souhaitant suivre le marché.

Son objectif principal est de fournir une base de données propre, structurée et prête pour l'analyse décisionnelle et la Business Intelligence.

---

# 3. Problématique

Le problème identifié est que les données immobilières brutes sur le web sont souvent éparpillées, mal structurées, contiennent des doublons ou des valeurs manquantes, ce qui rend l'analyse directe impossible pour les professionnels.

La solution proposée permet d'extraire automatiquement ces annonces, d'appliquer un nettoyage rigoureux à l'aide de scripts Python (Pandas), de charger les données structurées dans un entrepôt centralisé (PostgreSQL) et de les visualiser à travers un tableau de bord interactif.

---

# 4. Fonctionnalités principales

- Extraire les données brutes des annonces immobilières.
- Nettoyer les anomalies, formater les prix et traiter les valeurs manquantes avec Pandas.
- Structurer les données sous forme de modèle relationnel (Staging / BI).
- Charger automatiquement les données transformées dans PostgreSQL via SQLAlchemy.
- Visualiser les indicateurs clés (KPIs) du marché via un dashboard Power BI.

---

# 5. Technologies utilisées

Nous avons utilisé les technologies suivantes pour mener à bien le projet :

| Technologie | Utilisation dans le projet |
|-------------|----------------------------|
| Python | Langage principal pour l'écriture des scripts de pipeline |
| Pandas | Nettoyage, filtrage et transformation des données immobilières |
| PostgreSQL | Stockage et centralisation des données structurées |
| SQLAlchemy | Automatisation du chargement et connexion entre Python et la base[cite: 1] |
| Power BI | Conception du dashboard interactif et analyse visuelle[cite: 1] |
| GitHub | Versionnement et gestion du code source[cite: 1] |

---

# 6. Installation et lancement

## 6.1 Prérequis

Pour utiliser ce projet, vous devez disposer de :
- Python 3.8 ou supérieur[cite: 1]
- PostgreSQL[cite: 1]
- Power BI Desktop (pour ouvrir le rapport visuel)[cite: 1]
- Git[cite: 1]

---

## 6.2 Cloner le dépôt

```bash
git clone [https://github.com/Youssef-Jazouli/darkom-data-pipeline.git](https://github.com/Youssef-Jazouli/darkom-data-pipeline.git)
