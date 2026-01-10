from dash import Dash, html, dcc
from dash import dash_table
import pandas as pd
import plotly.express as px

# =========================
# Chargement des données
# =========================
df = pd.read_excel("MAL_dataset.xlsx")
# =========================
# Graphiques
# =========================

# Score par demographic
fig=[]
fig.append(
    px.histogram(
        df,
        x="Demographic",
        y="Score",
        histfunc="avg",
        title="Distribution de " + df.columns[0]
    ).update_xaxes(categoryorder='mean descending')
)

# Score par studios
fig.append(
    px.histogram(
        df,
        x="Studios",
        y="Score",
        histfunc="avg",
        title="Distribution de " + df.columns[0],
        category_orders={
        "Studios": df["Score"]}
    ).update_xaxes(categoryorder='mean descending')
)

# Score par type
fig.append(
    px.histogram(
        df,
        x="Type",
        y="Score",
        histfunc="avg",
        title="Distribution de " + df.columns[0],
        category_orders={
        "Studios": df["Score"]}
    ).update_xaxes(categoryorder='mean descending')
)

# Score par nombre d'episode
fig.append(
    px.scatter(
        df,
        x="Episodes",
        y="Score",
        title="Distribution de " + df.columns[0],
    )
)

# Score pour chaque saison de chaque année
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
        text_auto=True,
        aspect="auto",
        title="Score moyen par demographic et type"
    )
)

# Score par themes
ls_theme=[]
for e in df["Themes"]:
    if type(e)==str:
        for f in e.split(","):
            if f not in ls_theme:
                ls_theme.append(f)

theme_df = pd.DataFrame(columns=["Themes","Score"])
for e in ls_theme:
    score = df.loc[df['Themes'].str.contains(e, case=False, na=False), 'Score'].mean()
    theme_df.loc[len(theme_df)] = [e, score]

fig.append(
    px.histogram(
        theme_df,
        x="Themes",
        y="Score",
        title="Distribution de " + theme_df.columns[0],
        category_orders={
        "Themes": theme_df["Score"]}
    ).update_xaxes(categoryorder='mean descending')
)

# Score par genres
ls_genre=[]
for e in df["Genres"]:
    if type(e)==str:
        for f in e.split(","):
            if f not in ls_genre:
                ls_genre.append(f)

genre_df = pd.DataFrame(columns=["Genres","Score"])
for e in ls_genre:
    score = df.loc[df['Genres'].str.contains(e, case=False, na=False), 'Score'].mean()
    genre_df.loc[len(genre_df)] = [e, score]

fig.append(
    px.histogram(
        genre_df,
        x="Genres",
        y="Score",
        title="Distribution de " + genre_df.columns[0],
        category_orders={
        "Genres": genre_df["Score"]}
    ).update_xaxes(categoryorder='mean descending')
)

# Score par duree d'un episode
fig.append(
    px.scatter(
        df,
        x="Duration",
        y="Score",
        title="Distribution de " + df.columns[0],
    )
)

# Score par duree d'un episode
df['Total_Duration'] = df['Duration'] * df['Episodes']

fig.append(
    px.scatter(
        df,
        x="Total_Duration",
        y="Score",
        title="Distribution de " + df.columns[0],
    )
)

# Score par nombre de Membre
fig.append(
    px.histogram(
        df, 
        x="Members", 
        y="Score", 
        histfunc="avg", # Calcule la moyenne du score pour chaque tranche
        nbins=50,       # Ajuste le nombre de colonnes
        title="Score moyen selon la popularité (Membres)",
        labels={"Members": "Nombre de Membres", "Score": "Score Moyen"}
    )
)

# Score par nombre de Favorites
fig.append(
    px.histogram(
        df, 
        x="Favorites", 
        y="Score", 
        histfunc="avg", # Calcule la moyenne du score pour chaque tranche
        nbins=50,       # Ajuste le nombre de colonnes
        title="Score moyen selon la popularité (Membres)",
        labels={"Members": "Nombre de Membres", "Score": "Score Moyen"}
    )
)

# Score par nombre de Completed
fig.append(
    px.histogram(
        df, 
        x="Completed", 
        y="Score", 
        histfunc="avg", # Calcule la moyenne du score pour chaque tranche
        nbins=50,       # Ajuste le nombre de colonnes
        title="Score moyen selon la popularité (Membres)",
        labels={"Members": "Nombre de Membres", "Score": "Score Moyen"}
    )
)

# Score par nombre de ratio de Favorites / Members
df["Fav/Memb"]=df["Favorites"]/df["Members"]

fig.append(
    px.histogram(
        df, 
        x="Fav/Memb", 
        y="Score", 
        histfunc="avg", # Calcule la moyenne du score pour chaque tranche
        nbins=50,       # Ajuste le nombre de colonnes
        title="Score moyen selon la popularité (Membres)",
        labels={"Members": "Nombre de Membres", "Score": "Score Moyen"}
    )
)

# =========================
# App Dash
# =========================
app = Dash(__name__)

app.layout = html.Div([

    html.H1("Dashboard Dash", style={"textAlign": "center"}),

    # ---- Zone GRAPHIQUES ----
    html.Div([dcc.Graph(figure=e) for e in fig],
        style={
        "display": "grid",
        "gridTemplateColumns": "1fr 1fr",
        "gap": "20px"
    }),

    html.Hr(),

    # ---- Zone TABLE ----
    dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": col, "id": col} for col in df.columns],
        page_size=15,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left"}
    )
])

# =========================
# Lancement
# =========================
if __name__ == "__main__":
    app.run(debug=True)