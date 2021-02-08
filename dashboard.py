import plotly          
# import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import config
import meraki
import pandas as pd


api_key = config.api_key

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def createLayout():
    dropdown_items = [
        {'label': 'Table 1', 'value': '101'},
        {'label': 'Table 2', 'value': '102'},
        {'label': 'Table 3', 'value': '103'},
        {'label': 'Table 4', 'value': '104'},
        {'label': 'Table 5', 'value': '105'},
        {'label': 'Table 6', 'value': '106'},
        {'label': 'Table 7', 'value': '107'},
        {'label': 'Table 8', 'value': '108'}
    ]
    app.layout = html.Div([
        dbc.Row(
            dbc.Col(
                html.Div(
                    html.H1('Prov Table Clients'),
                    id = 'header'
                ),
                width = {'size': 6, 'offset': 3}
            )
        ),
        dbc.Row([
            dbc.Col(
                html.Div(
                    dcc.Dropdown(
                        id = 'table-dropdown',
                        options = dropdown_items,
                        placeholder = 'Select a table...'
                    )
                ),
                width = {'size': 2, 'offset': 3}
            ),
            dbc.Col(
                html.Div([
                    html.H3(
                        children = 'DHCP Option',
                        id = 'dhcp-option-h3'
                    ),
                    html.P(
                        children = 'Select a table...',
                        id = 'dhcp-option-p'
                    )
                ])
            )
        ]),
        dbc.Row(
            dbc.Col(
                html.Div(
                    dash_table.DataTable(
                        id = 'clients-table',
                        columns = [
                            {'name': 'Description', 'id': 'description'},
                            {'name': 'MAC Address', 'id': 'mac'},
                            {'name': 'IP Address', 'id': 'ip'}
                        ],
                        style_header = {'background': '#333'},
                        style_cell = {'background': '#444'}
                    ),
                ),
                width = {'size': 6, 'offset': 3}
            )
        ),
        dcc.Interval(
        id = 'client-interval',
        interval = 5 * 1000,
        n_intervals = 0
    )
    ],
    id = 'container')

createLayout()

dashboard = meraki.DashboardAPI(
        api_key=api_key,
        base_url='https://api-mp.meraki.com/api/v1/',
        print_console=False,
        output_log=False
    )

network = 'L_613052499275810377'


@app.callback(
    Output('dhcp-option-p', 'children'),
    [Input('client-interval', 'n_intervals'),
    Input('table-dropdown', 'value')]
)
def getVlans(num, value):
    if value == None:
        value = 101
    try:
        # Get list of clients on network, filtering on timespan of last 14 days
        vlans = dashboard.appliance.getNetworkApplianceVlans(network)
    except meraki.APIError as e:
        print(f'Meraki API error: {e}')
        print(f'status code = {e.status}')
        print(f'reason = {e.reason}')
        print(f'error = {e.message}')
    except Exception as e:
        print(f'some other error: {e}')

    for vlan in vlans:
        if vlan['id'] == int(value) and 'dhcpOptions' in vlan:
            print(f'Selected VLAN: {vlan["id"]}')
            for option in vlan['dhcpOptions']:
                dhcp_option = option['value']
                print(dhcp_option)
        elif 'dhcpOptions' not in vlan:
            dhcp_option = 'UNSET'

    return dhcp_option


@app.callback(
    Output('clients-table', 'data'),
    [Input('client-interval', 'n_intervals'),
    Input('table-dropdown', 'value')]
)
def getClients(num, value):
    if value == None:
        value = 101
    try:
        # Get list of clients on network, filtering on timespan of last 14 days
        clients = pd.DataFrame(dashboard.networks.getNetworkClients(network, timespan=60*60*24*1, perPage=1000, total_pages='all'))
    except meraki.APIError as e:
        print(f'Meraki API error: {e}')
        print(f'status code = {e.status}')
        print(f'reason = {e.reason}')
        print(f'error = {e.message}')
    except Exception as e:
        print(f'some other error: {e}')
    
    print(f'Selected Table: {value}')

    filtered_clients = clients.loc[clients['vlan'] == int(value)]
    print(filtered_clients)

    return filtered_clients.to_dict('records')


if __name__ == '__main__':
    app.run_server(
        host='0.0.0.0',
        port='8051',
        debug=True
    )