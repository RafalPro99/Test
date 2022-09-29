from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd

# Data: https://www.dallasopendata.com/Services/Animals-Inventory/qgg6-h4bd
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Analytic_Web_Apps/Excel_to_Dash_Animal_Shelter/Animals_Inventory.csv")
df["intake_time"] = pd.to_datetime(df["intake_time"])
df["intake_time"] = df["intake_time"].dt.hour

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Analytics Dashboard of Dallas Animal Shelter (Dash Plotly)", style={"textAlign":"center"}),
    html.Hr(),
    html.P("Choose animal of interest:"),
    html.Div(html.Div([
        dcc.Dropdown(id='animal-type', clearable=False,
                     value="DOG",
                     options=[{'label': x, 'value': x} for x in
                              df["animal_type"].unique()]),
    ],className="two columns"),className="row"),

    html.Div(id="output-div", children=[]),
])


@app.callback(Output(component_id="output-div", component_property="children"),
              Input(component_id="animal-type", component_property="value"),
)
def make_graphs(animal_chosen):
    # HISTOGRAM
    df_hist = df[df["animal_type"]==animal_chosen]
    fig_hist = px.histogram(df_hist, x="animal_breed")
    fig_hist.update_xaxes(categoryorder="total descending")


    return [
        html.Div([
            html.Div([dcc.Graph(figure=fig_hist)], className="six columns"),
        ], className="row"),

    ]


if __name__ == '__main__':
    app.run_server(debug=False, port=1212)
