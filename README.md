# Collecte et Traitement de données MyAnimeList

Ce projet est un outil de **Web Scraping** conçu pour extraire, nettoyer et centraliser des informations détaillées sur les animés depuis le site [MyAnimeList](https://myanimelist.net/).

Les données passent par un processus de transformation (conversion des durées en minutes, gestion des saisons, nettoyage des doublons) avant d'être exportées dans un fichier Excel exploitable pour de l'analyse de données.

Une WebApp interactive est mise à disposition pour visualiser les données selon plusieurs axes (temporels, thématiques, etc.). Elle permet d'explorer les résultats de l'analyse de manière intuitive.

## 🚀 Fonctionnalités

* **Collecte automatisée :** Extraction des informations techniques (Score, Rank, Studios, Genres, Durée, etc.).
* **Nettoyage Intelligent :**
    * Conversion des formats de durée complexes (ex: "24 min per ep" ou "1 hr 30 min" en minutes entières).
    * Extraction de la saison et de l'année à partir des dates de diffusion.
    * Suppression des doublons textuels dans les genres et thèmes.
    * Conversion des nombres au format "anglo-saxon" (virgules pour les milliers) en entiers manipulables.
* **Export :** Génération d'un dataset propre au format `.xlsx`.
* **Visualisation :** Représentation graphique des données permettant d'illustrer les résultats de manière interactive.

## 🛠️ Installation (Mise en place chez soi)

### 1. Prérequis

Assurez-vous d'avoir **Python 3.8** ou une version supérieure installée sur votre machine.

### 2. Cloner le projet

Téléchargez le dossier ou utilisez Git :

```bash
git clone https://github.com/votre-compte/sae-vcod-1.git
```

### 3. Installer les bibliothèques nécessaires

Le projet utilise différentes bibliothèques pour le traitement de données et l'affiche :

```bash
pip install -r requirements.txt
```
OU
```bash
pip install pandas
```
```bash
pip install openpyxl
```
```bash
pip install dash
```
```bash
pip install bs4
```
```bash
pip install requests
```

## ⚙️ Structure des fichiers

* `main.py` : Script de lancement principal (interface ou orchestration).
* `ETL.py` : Le cœur du traitement. Il contient les fonctions de nettoyage et transforme les fichiers textes bruts en tableau Excel.
* `GetPage.py` : Module responsable de la récupération des données sur MyAnimeList.
* `/donneMAL` : **Dossier source.** C'est ici que se trouve les fichiers `.txt` bruts (un fichier par animé) récupérés lors du scraping.

## 🚀 Utilisation

Lancez les scripts de recolte et de traitement dans l'ordre :
```bash
python GetPage.py
python ETL.py
```

3. Une fois terminé, le message `✔ Export terminé` s'affichera et vous trouverez le fichier **`MAL_dataset.xlsx`** à la racine de votre dossier.

4. Vous pouvez maintenant lancer la WebApp qui permetras de visualiser les graphiques
```bash
python App.py
```

## 📊 Données traitées

Le dataset final inclut les colonnes suivantes :

*  **Name** : Le titre original de l'animé (récupéré à partir du nom du fichier source).
*  **English** : Le titre officiel en anglais, si disponible.
*  **Type** : Le format de diffusion (ex: TV, Movie, OVA, Special).
*  **Episodes** : Le nombre total d'épisodes (converti en nombre entier ; Unknown est traité comme vide).
*  **Studios** : Le studio d'animation principal (seul le premier studio est conservé pour simplifier l'analyse).
*  **Themes** : Liste des thèmes associés à l'œuvre (nettoyés des répétitions textuelles).
*  **Demographic** : La cible démographique principale (ex: Shounen, Seinen, Shoujo, Josei).
*  **Duration** : La durée de l'animé convertie uniformément en minutes (ex: "1 hr 20 min" devient 80).
*  **Score** : La note moyenne attribuée par les utilisateurs de MyAnimeList (format numérique sur 10).
*  **Members** : Le nombre total d'utilisateurs ayant ajouté l'animé à leur liste (format entier).
*  **Favorites** : Le nombre d'utilisateurs ayant marqué l'œuvre comme "Favorite" (format entier).
*  **Completed** : Le nombre de personnes ayant fini de visionner l'œuvre (format entier).
*  **Season** : La saison de sortie (Spring, Summer, Fall, Winter), extraite de la date de première diffusion.
*  **Year** : L'année de sortie (format numérique), extraite pour permettre des tris chronologiques.
*  **Genres** : Catégories de l'œuvre (ex: Action, Sci-Fi) avec suppression des doublons.


## Répartition du travail

Nous avons réparti les tâches de la manière suivante :

* Partie 1 : Extraction des données

    * Mattéo a développé le code permettant d'extraire les informations depuis les pages web.

    * Timéo s'est chargé de l'analyse de la structure de ces pages.

* Partie 2 : Traitement des données

    * Timéo a traité les données récupérées afin de les regrouper dans un fichier structuré.

* Partie 3 : Visualisation et Analyse

    * Mattéo a sélectionné les graphiques pertinents et a développé la WebApp pour les afficher.

    * Timéo a analysé les résultats obtenus afin de compléter le rapport final.