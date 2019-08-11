import boto3
import os
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Mexique 2019'

def serve_layout():

    prix_original = 4317

    #Connect to AWS
    session = boto3.Session(
        aws_access_key_id=os.environ['aws_access_id'],
        aws_secret_access_key=os.environ['aws_access_secret']
    )

    dynamodb = session.resource('dynamodb',region_name='us-east-1')
    table = dynamodb.Table('trip_price')

    #Get raw data from DynamoDB and push it into a dict
    raw_data = {}
    for x in table.scan()['Items']:
        raw_data[x['time']] = x['total_price']
        

    #Original proce
    ordered_data = [[datetime.datetime.strptime('2019-06-14 12:00:00', '%Y-%m-%d %H:%M:%S')], [prix_original]]

    #Load all into a sorted 2D list
    for key in sorted(raw_data.keys()):
        ordered_data[0].append(datetime.datetime.strptime(key, '%Y-%m-%d %H:%M:%S'))
        ordered_data[1].append(int(raw_data[key]))
    
    current_price = ordered_data[1][len(ordered_data[1])-1]

    abs_diff = current_price - prix_original

    rel_divv = abs_diff/prix_original*100

    price = ""

    if (current_price > prix_original):
        # more expensive
        price = html.Div([
            html.P('Le prix courant du voyage est de '),
            html.Div([
                html.P(str(current_price) + '$', style={'color': 'green', 'font-size': '25pt'})
            ]),
            html.P('C\'est une augmentation de '+ str(abs_diff)+'$ ('+str.format("{0:.1f}", rel_divv)+'%)'),
            html.P('Basé sur un prix d\'achat de 4317$'),
        ], style={'width': '1000px', 'margin-top': '0px', 'margin-bottom': '0px', 'margin-left': 'auto', 'margin-right': 'auto', 'background-color': '#EEEEEE', 'text-align': 'center', 'padding': '20px 20px 20px 20px'})
    else:
        #CHEAPER
        price = html.Div([
            html.P('Le prix courant du voyage est de '),
            html.Div([
                html.P(str(current_price) + '$', style={'color': 'red', 'font-size': '25pt'})
            ]),
            html.P('C\'est une diminution de '+ str(abs_diff)+'$ ('+str.format("{0:.1f}", rel_divv)+'%)'),
            html.P('Basé sur un prix d\'achat de 4317$'),
        ], style={'width': '1000px', 'margin-top': '0px', 'margin-bottom': '0px', 'margin-left': 'auto', 'margin-right': 'auto', 'background-color': '#EEEEEE', 'text-align': 'center', 'padding': '20px 20px 20px 20px'})

    return_html = html.Div(children=[
        html.H1(children='Prix Voyage au Mexique 2019' , style={'width': '1000px', 'margin-top': '30px', 'margin-bottom': '30px', 'margin-left': 'auto', 'margin-right': 'auto', 'background-color': '#EEEEEE', 'text-align': 'center', 'padding': '20px 20px 20px 20px'}),
    
        price,
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': ordered_data[0], 'y': ordered_data[1], 'type': 'line'},
                ],
                'layout': {
                    'title': 'Évolution du prix du voyage'
                }
            }, 
            style={'width': '1000px', 'margin-top': '30px', 'margin-bottom': '30px', 'margin-left': 'auto', 'margin-right': 'auto', 'background-color': '#EEEEEE', 'text-align': 'center', 'padding': '20px 20px 20px 20px'}
        )
    ], style={'text-align': 'center'})
        
    return return_html

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0')