# MyAnimeList Data Collector & Processor

Ce projet est un outil de **Web Scraping** et d'**ETL** (Extract, Transform, Load) conçu pour extraire, nettoyer et centraliser des informations détaillées sur les animés depuis le site [MyAnimeList](https://myanimelist.net/).

Les données passent par un processus de transformation (conversion des durées en minutes, gestion des saisons, nettoyage des doublons) avant d'être exportées dans un fichier Excel exploitable pour de l'analyse de données.

## 🚀 Fonctionnalités

* **Collecte automatisée :** Extraction des informations techniques (Score, Rank, Studios, Genres, Durée, etc.).
* **Nettoyage Intelligent (ETL) :**
* Conversion des formats de durée complexes (ex: "24 min per ep" ou "1 hr 30 min" en minutes entières).
* Extraction de la saison et de l'année à partir des dates de diffusion.
* Suppression des doublons textuels dans les genres et thèmes.
* Conversion des nombres au format "anglo-saxon" (virgules pour les milliers) en entiers manipulables.


* **Export :** Génération d'un dataset propre au format `.xlsx`.

## 🛠️ Installation (Mise en place chez soi)

### 1. Prérequis

Assurez-vous d'avoir **Python 3.8** ou une version supérieure installée sur votre machine.

### 2. Cloner le projet

Téléchargez le dossier ou utilisez Git :

```bash
git clone https://github.com/votre-compte/sae-vcod-1.git
cd sae-vcod-1-Matteo

```

### 3. Installer les bibliothèques nécessaires

Le projet utilise `pandas` pour le traitement de données et `openpyxl` pour la création du fichier Excel :

```bash
pip install pandas openpyxl

```

## ⚙️ Structure des fichiers

* `main.py` : Script de lancement principal (interface ou orchestration).
* `ETL.py` : Le cœur du traitement. Il contient les fonctions de nettoyage et transforme les fichiers textes bruts en tableau Excel.
* `GetPage.py` : Module responsable de la récupération des données sur MyAnimeList.
* `/donneMAL` : **Dossier source.** C'est ici que vous devez placer vos fichiers `.txt` bruts (un fichier par animé) récupérés lors du scraping.

## 🚀 Utilisation

1. Placez vos fichiers bruts dans le dossier `donneMAL/`.
2. Lancez le script de traitement :
```bash
python ETL.py

```


3. Une fois terminé, le message `✔ Export terminé` s'affichera et vous trouverez le fichier **`MAL_dataset.xlsx`** à la racine de votre dossier.

## 📊 Données traitées

Le dataset final inclut les colonnes suivantes :

* **Name** : Titre de l'œuvre.
* **Score** : Note moyenne sur 10.
* **Duration** : Durée totale convertie en minutes (numérique).
* **Season / Year** : Saison de sortie et année (séparées pour filtrage facile).
* **Members / Favorites** : Statistiques de popularité.
* **Episodes** : Nombre total d'épisodes (formaté en entier).

---

*Ce projet a été réalisé dans le cadre d'un projet Unniversitaire*