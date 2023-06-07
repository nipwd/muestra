import dash
from dash import dcc
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Mi dashboard'),
    dcc.Graph(
        id='mi-grafico',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Ciudad A'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Ciudad B'},
            ],
            'layout': {
                'title': 'Comparación de ciudades'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
