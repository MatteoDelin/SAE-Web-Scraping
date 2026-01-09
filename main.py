import GetPage as gp
from dash import Dash, html, dcc
from dash import dash_table
import pandas as pd
import plotly.express as px

# =========================
# Chargement des données
# =========================
df = pd.read_excel("MAL_dataset.xlsx")
# =========================
# Graphiques (créés au lancement)
# =========================

# Exemple 1 : histogramme
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

fig.append(
    px.scatter(
        df,
        x="Episodes",
        y="Score",
        title="Distribution de " + df.columns[0],
    )
)

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