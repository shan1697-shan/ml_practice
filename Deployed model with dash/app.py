from dash import Dash, dcc, html, Input, Output, State, DiskcacheManager, dash_table
import dash_bootstrap_components as dbc
import pickle
import dash
from helper import models_path_map, parse_data
import diskcache
import pandas as pd

cache = diskcache.Cache("/cache")
background_callback_manager = DiskcacheManager(cache)

app = Dash(__name__, background_callback_manager=background_callback_manager, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    dbc.Row([html.H2("Prediction Dashboard")],style={'text-align':'center'}),
    dbc.Row([
        dbc.Col([dcc.Dropdown(['Linear Regression', 'Lars and Lasso Regression', 
                    "Decision Tree Regression", "Decision Tree(Hyperparameters)", 
                    "Random Forest"], 
                'Linear Regression', id='model_dropdown'),
                ], width=12),
        dbc.Col([
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
            ),
        ], width=12),
        dbc.Col(
            dbc.Button("Predict", id='predict_btn'),width=2, style={'padding-bottom':"2%"}
        ),
        dbc.Col(
            dbc.Progress(id='progress_bar',animated=True, striped=True, style={"visibility": "hidden"}),
            style={'padding-bottom':"2%"}, width=12
        ),
        dbc.Col(
            dbc.Button("Cancel Button", id='cancel_button_id'), width=12
        ),
        html.Div(id='prediction_output', style={'padding-top':"2%"})
    ], style={'padding-left':"5%", "padding-right":"5%", 'padding-bottom':"2%"}),
    
])


@dash.callback(
    output=[
        Output('prediction_output', 'children'),
    ],
    inputs=[
        Input('predict_btn','n_clicks')
    ],
    state = [
        State('model_dropdown', 'value'),
        State('upload-data', 'contents'),
        State('upload-data', 'filename')
    ],
    background=True,
    running=[
        (
            Output("progress_bar", "style"),
            {"visibility": "visible"},
            {"visibility": "hidden"},
        ),
    ],
    cancel=Input("cancel_button_id", "n_clicks"),
    progress=[Output("progress_bar", "value"), Output("progress_bar", "label")],
    prevent_initial_call=True
)
def update_output(set_progress, predict_btn, model_type, file, filename):
    if model_type is None or file is None:
        return dash.no_update
    model_path = models_path_map[model_type]+'/model.sav'
    set_progress((10, '10%'))
    model = pickle.load(open(model_path, 'rb'))
    set_progress((25, '25%'))
    data = parse_data(file, filename)
    set_progress((35, '35%'))
    prediction = model.predict(data)
    set_progress((75, '75%'))
    data['predictions'] = prediction
    result = dash_table.DataTable(data.to_dict('records'), [{"name": i, "id": i} for i in data.columns[::-1]])
    set_progress((100, '100%'))

    return [result]


if __name__ == '__main__':
    app.run_server(debug=True)