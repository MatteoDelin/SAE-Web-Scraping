# =========================
# Imports
# =========================

# Composants principaux de Dash
from dash import Dash, html, dcc

# Tableau interactif Dash
from dash import dash_table

# Manipulation de données
import pandas as pd

# Graphiques Plotly
import plotly.express as px
import seaborn as sns

# =========================
# Chargement des données
# =========================

# Chargement du dataset MyAnimeList depuis le fichier Excel
df = pd.read_excel("MAL_dataset.xlsx")


# =========================
# Création des graphiques
# =========================

# Liste qui contiendra tous les graphiques
fig = []


# -------------------------------------------------
# Score moyen par demographic
# -------------------------------------------------
fig.append(
    px.histogram(
        df,
        x="Demographic",
        y="Score",
        histfunc="avg",  # Calcul de la moyenne des scores
        title="Score moyen par demographie"
    ).update_xaxes(categoryorder='mean descending')
)


# -------------------------------------------------
# Score moyen par studio
# -------------------------------------------------
fig.append(
    px.histogram(
        df,
        x="Studios",
        y="Score",
        histfunc="avg",
        title="Score moyen par studio",
        category_orders={
            "Studios": df["Score"]
        }
    ).update_xaxes(categoryorder='mean descending')
)


# -------------------------------------------------
# Score moyen par type d'anime
# -------------------------------------------------
fig.append(
    px.histogram(
        df,
        x="Type",
        y="Score",
        histfunc="avg",
        title="Score moyen par type d'anime",
        category_orders={
            "Studios": df["Score"]
        }
    ).update_xaxes(categoryorder='mean descending')
)


# -------------------------------------------------
# Score en fonction du nombre d'épisodes
# -------------------------------------------------
fig.append(
    px.scatter(
        df,
        x="Episodes",
        y="Score",
        title="Score en fonction du nombre d'épisodes",
    )
)


# -------------------------------------------------
# Score moyen par saison et par année (heatmap)
# -------------------------------------------------
heatmap_df = pd.pivot_table(
    df,
    values="Score",
    index="Year",
    columns="Season",
    aggfunc="mean"
)

fig.append(
    px.imshow(
        heatmap_df,
        text_auto=".2f",
        aspect="equal",
        color_continuous_scale="YlOrRd",
        title="Score moyen par saison et par année"
    )
    .update_traces(
        textfont=dict(
            size=14,
            color="black"
        )
    )
    .update_layout(
        height=1000,
        width=1100
    )
)

# -------------------------------------------------
# Score moyen par thème
# -------------------------------------------------

# Extraction de tous les thèmes uniques
ls_theme = []
for e in df["Themes"]:
    if isinstance(e, str):
        for f in e.split(","):
            if f not in ls_theme:
                ls_theme.append(f)

# Calcul du score moyen par thème
theme_df = pd.DataFrame(columns=["Themes", "Score"])
for e in ls_theme:
    score = df.loc[
        df['Themes'].str.contains(e, case=False, na=False),
        'Score'
    ].mean()
    theme_df.loc[len(theme_df)] = [e, score]

fig.append(
    px.histogram(
        theme_df,
        x="Themes",
        y="Score",
        title="Score moyen par thème",
        category_orders={
            "Themes": theme_df["Score"]
        }
    ).update_xaxes(categoryorder='mean descending')
)


# -------------------------------------------------
# Score moyen par genre
# -------------------------------------------------

# Extraction de tous les genres uniques
ls_genre = []
for e in df["Genres"]:
    if isinstance(e, str):
        for f in e.split(","):
            if f not in ls_genre:
                ls_genre.append(f)

# Calcul du score moyen par genre
genre_df = pd.DataFrame(columns=["Genres", "Score"])
for e in ls_genre:
    score = df.loc[
        df['Genres'].str.contains(e, case=False, na=False),
        'Score'
    ].mean()
    genre_df.loc[len(genre_df)] = [e, score]

fig.append(
    px.histogram(
        genre_df,
        x="Genres",
        y="Score",
        title="Distribution de " + genre_df.columns[0],
        category_orders={
            "Score moyen par genre"
        }
    ).update_xaxes(categoryorder='mean descending')
)


# -------------------------------------------------
# Score en fonction de la durée d'un épisode
# -------------------------------------------------
fig.append(
    px.scatter(
        df,
        x="Duration",
        y="Score",
        title="Score en fonction de la durée d'un épisode",
    )
)


# -------------------------------------------------
# Score en fonction de la durée totale (durée * épisodes)
# -------------------------------------------------

# Création de la durée totale
df['Total_Duration'] = df['Duration'] * df['Episodes']

fig.append(
    px.scatter(
        df,
        x="Total_Duration",
        y="Score",
        title="Score en fonction de la durée totale (durée * épisodes)",
    )
)


# -------------------------------------------------
# Score moyen selon le nombre de membres
# -------------------------------------------------
fig.append(
    px.histogram(
        df,
        x="Members",
        y="Score",
        histfunc="avg",
        nbins=50,
        title="Score moyen selon le nombre de membres",
        labels={"Members": "Nombre de Membres", "Score": "Score Moyen"}
    )
)


# -------------------------------------------------
# Score moyen selon le nombre de favoris
# -------------------------------------------------
fig.append(
    px.histogram(
        df,
        x="Favorites",
        y="Score",
        histfunc="avg",
        nbins=50,
        title="Score moyen selon le nombre de favoris",
        labels={"Favorites": "Nombre de Favoris", "Score": "Score Moyen"}
    )
)


# -------------------------------------------------
# Score moyen selon le nombre de complétions
# -------------------------------------------------
fig.append(
    px.histogram(
        df,
        x="Completed",
        y="Score",
        histfunc="avg",
        nbins=50,
        title="Score moyen selon le nombre de complétions",
        labels={"Completed": "Nombre de complétions", "Score": "Score Moyen"}
    )
)


# -------------------------------------------------
# Score selon le ratio Favoris / Membres
# -------------------------------------------------

# Calcul du ratio
df["Fav/Memb"] = df["Favorites"] / df["Members"]

fig.append(
    px.histogram(
        df,
        x="Fav/Memb",
        y="Score",
        histfunc="avg",
        nbins=50,
        title="Score selon le ratio Favoris / Membres"
    )
)

# =========================
# Application Dash
# =========================

app = Dash(__name__)

app.layout = html.Div([

    # Titre principal
    html.H1("Dashboard Dash", style={"textAlign": "center"}),

    # -------------------------------------------------
    # Zone des graphiques
    # -------------------------------------------------
    html.Div(
        [dcc.Graph(figure=e) for e in fig],
        style={
            "display": "grid",
            "gridTemplateColumns": "1fr",
            "gap": "20px"
        }
    ),

    html.Hr(),

    # -------------------------------------------------
    # Tableau interactif
    # -------------------------------------------------
    dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": col, "id": col} for col in df.columns],
        page_size=15,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left"}
    )
])


# =========================
# Lancement de l'application
# =========================
if __name__ == "__main__":
    app.run(debug=True)
