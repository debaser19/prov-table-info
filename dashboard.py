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


api_key = config.api_key

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

dashboard = meraki.DashboardAPI(
        api_key=api_key,
        base_url='https://api-mp.meraki.com/api/v1/',
        print_console=False,
        output_log=False
    )

network = 'L_613052499275810377'
table_id = 107
list_of_clients = []

dhcp_option = '<em>UNSET</em>'

def getVlans():
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
    else:
        print(vlans)
        for vlan in vlans:
            if vlan['id'] == table_id and 'dhcpOptions' in vlan:
                for option in vlan['dhcpOptions']:
                    dhcp_option = option['value']


def getClients():
    # TODO: Grab list of clients from VLAN depending on dropdown selection
    return


app.layout = html.Div(
    html.H1('Hi')
)


if __name__ == '__main__':
    app.run_server(
        host='0.0.0.0',
        port='8051',
        debug=True
    )