import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import json

# Load data from the JSON file
with open('data.json', 'r') as f:
    data = json.load(f)

evse_data = data['body']['evse_data']
registered_cps = data['body']['registered_cps']
waiting_cps = data['body']['waiting_cps']

app = dash.Dash(__name__)

# Sidebar style
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# Content style
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("EVSE Dashboard", className="display-4"),
        html.Hr(),
        html.P(
            "Select Data:", className="lead"
        ),
        dcc.Dropdown(
            id='data-type-dropdown',
            options=[
                {'label': 'EVSE Data', 'value': 'evse_data'},
                {'label': 'Registered CPS', 'value': 'registered_cps'},
                {'label': 'Waiting CPS', 'value': 'waiting_cps'}
            ],
            value='evse_data'  # Default selected value
        ),
        html.Hr(),
        html.P("Additional filters or options can go here.", className="lead"),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(
    Output("page-content", "children"),
    [Input('data-type-dropdown', 'value')]
)
def update_dashboard(data_type):
    if data_type == 'evse_data':
        df = pd.DataFrame(evse_data)
        fig = px.bar(df, x='operator_id', y='total_countries',
                     title='Total Countries by Operator')

    elif data_type == 'registered_cps':
        df = pd.DataFrame(registered_cps)
        fig = px.bar(df, x='operator_id', y='count',
                     title='Registered CPS Count by Operator')

    elif data_type == 'waiting_cps':
        df = pd.DataFrame(waiting_cps)
        fig = px.bar(df, x='operator_id', y='count',
                     title='Waiting CPS Count by Operator')
    else:
        return html.Div("Invalid data type selected.")

    return dcc.Graph(figure=fig)

if __name__ == '__main__':
    app.run_server(debug=True)
