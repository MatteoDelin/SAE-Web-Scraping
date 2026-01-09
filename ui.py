import dash
from dash import html

# Initialisation de l'app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Dash", style={"textAlign": "center"}),

    html.Button("Afficher le DataFrame", id="btn-load"),

    html.Div(
        html.Table(id="table-df"),
        style={"width": "80%", "margin": "auto"}
    )
])

