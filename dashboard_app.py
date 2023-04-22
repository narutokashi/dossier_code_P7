import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import pickle, joblib
import plotly.graph_objs as go
import shap

# Load the data and model
df = pd.read_csv('data_api.csv')
model = joblib.load(open('trained_ppl.pkl', 'rb'))

shap_values = {}
shap_values = joblib.load(open('shap_values_test.pkl', 'rb'))

def force_plot_html(*args):
    force_plot = shap.force_plot(*args, matplotlib=False)
    shap_html = f"<head>{shap.getjs()}</head><body>{force_plot.html()}</body>"
    return html.Iframe(srcDoc=shap_html,
                      style ={"width":"100%", "height":"800px", "border":1})

# Create the app
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])
server = app.server

select_client = dbc.Card([html.Div([dbc.Label("Client ID"),
                                  dcc.Dropdown(id="Client ID", options=df['SK_ID_CURR'].values,
                                               multi=False, value=100001)])], body=True)


# Define the layout
# Define the layout
app.layout = dbc.Container([html.H1('Credit Score', className='text-center mb-4'),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader('Client ID'), select_client,

                html.Div(dcc.Graph(id='gauge-chart', figure={}), className='mt-4')
            ], className='text-center'),
            width=12
        )
    ], className='mt-4'),
    dbc.Row([
        dbc.Col(
            dbc.Card([html.Div(dcc.Graph(id='fig-profile', figure={}), className='mt-4')
            ], className='text-center'),
            width=12
        )
    ], className='text-center'),
    dbc.Row([
            dbc.Col(dbc.Card([dbc.CardHeader('SHAP Feature Explainer'), html.Div(id='shap')],
                                                 className='text-center'), width=5),
            dbc.Col(dbc.Card([dbc.CardHeader('Feature Global Importance'),
                        dcc.Graph(id='summ-shap')], className='text-center'), width=5)],
                                # align='center',
                                className='text-center')

], fluid=True)

# Define the callback for the button
@app.callback((
    Output('gauge-chart', 'figure'),
    Output('fig-profile', 'figure'),
    Output('shap', 'children'),
    Output('summ-shap', 'figure')),
    Input(component_id='Client ID', component_property='value')
)

def predict(client_id):
    # # Check if the button has been clicked
    # if n_clicks == 0:
    #     return {}

    # Get the row corresponding to the client_id
    row = df[df['SK_ID_CURR'] == client_id]

    # Check if the client_id exists in the dataset
    if row.empty:
        return {}

    # Make the prediction
    X = df[df['SK_ID_CURR'] == client_id].iloc[:, 1:]
    score = model.predict_proba(X)[0][1]
    pred = model.predict(X)[0]

    # Set the loan status based on the predicted value
    if pred < 0.5:
        loan_status = 'Accepted'
    else:
        loan_status = 'Rejected'
    loan_status_text = f"Loan status: {loan_status}"

    # Define the gauge chart
    gauge_chart = {
        'data': [{
            'type': 'indicator',
            'value': score,
            'delta': {'reference': 0.5},
            'gauge': {
                'axis': {'range': [None, 1]},
                'steps': [
                    {'range': [0, 0.5], 'color': '#13e13c'},
                    {'range': [0.5, 1], 'color': '#FF5733'}
                ],
                'threshold': {'line': {'color': '#1428f0', 'width': 4}, 'thickness': 0.75, 'value': 0.5},
                'bar': {'color': 'black'}
            },
            'mode': 'gauge+number',
            'title': {'text': f"{loan_status_text}", 'font' : {'size':30}}
        }]
    }

    # fig_client
    # Get the corresponding row from the test data
    row = df[df['SK_ID_CURR'] == client_id].iloc[:, 1:]

    # Get the feature values
    feature_values = row[['DAYS_BIRTH',
                     'EXT_SOURCE_1',
                     'EXT_SOURCE_2',
                     'EXT_SOURCE_3',
                     'BURO_DAYS_CREDIT_MEAN',
                     'BURO_DAYS_CREDIT_UPDATE_MEAN',
                     'BURO_CREDIT_ACTIVE_Active_MEAN',
                     'PREV_NAME_CONTRACT_STATUS_Refused_MEAN']].values.tolist()[0]

    # Create a bar chart using the feature values
    fig_client = go.Figure(
        data=[go.Bar(x=['DAYS_BIRTH',
                     'EXT_SOURCE_1',
                     'EXT_SOURCE_2',
                     'EXT_SOURCE_3',
                     'BURO_DAYS_CREDIT_MEAN',
                     'BURO_DAYS_CREDIT_UPDATE_MEAN',
                     'BURO_CREDIT_ACTIVE_Active_MEAN',
                     'PREV_NAME_CONTRACT_STATUS_Refused_MEAN'],
                     y=feature_values)],
        layout_title_text='Client Features'
    )

    data = df[df['SK_ID_CURR'] == client_id]
    idx = data.index.values
    shap_html = force_plot_html(shap_values[idx])

    fig_shap = go.Figure(data=go.Scatterpolar(r=[ 0.04530796, -0.27021242, -0.5658526 , -0.47969472, -0.02236737,
        0.02951732,  0.03680467,  0.19357835],
                                              theta=['PREV_NAME_CONTRACT_STATUS_Refused_MEAN', 'DAYS_BIRTH',
                                                     'BURO_CREDIT_ACTIVE_Active_MEAN', 'BURO_DAYS_CREDIT_UPDATE_MEAN',
                                                     'BURO_DAYS_CREDIT_MEAN', 'EXT_SOURCE_1',
                                                     'EXT_SOURCE_3', 'EXT_SOURCE_2']))

    fig_shap.update_traces(fill='toself')
    fig_shap.update_layout(
        polar=dict(
            #         radialaxis_angle = 0,
            angularaxis=dict(
                direction='clockwise',
                period=6)
        ))

    return gauge_chart, fig_client, shap_html, fig_shap

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)