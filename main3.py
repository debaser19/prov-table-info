import meraki
import creds
import json
import os

API_KEY = creds.creds['api_key']

def main():
    dashboard = meraki.DashboardAPI(
        api_key = API_KEY,
        base_url='https://api-mp.meraki.com/api/v1/',
        print_console=False,
        output_log=False
    )

    network = 'L_613052499275810377'

    table_id = 108
    list_of_clients = []
    table_body_string = ''
    table_body_close = '''
        </tbody>
        </table>
        </center>
    '''
    dhcp_option = '<em>UNSET</em>'
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
        for vlan in vlans:
            if vlan['id'] == table_id and 'dhcpOptions' in vlan:
                for option in vlan['dhcpOptions']:
                    dhcp_option = option['value']

    try:
        # Get list of clients on network, filtering on timespan of last 14 days
        clients = dashboard.networks.getNetworkClients(network, timespan=60*60*24*1, perPage=1000, total_pages='all')
    except meraki.APIError as e:
        print(f'Meraki API error: {e}')
        print(f'status code = {e.status}')
        print(f'reason = {e.reason}')
        print(f'error = {e.message}')
    except Exception as e:
        print(f'some other error: {e}')
    else:
        counter = 1
        for client in clients:
            # need to alternate  the background colour of the td based on counter % 0 for evens
            if counter % 2 == 0:
                tg_class = 'tg-alz1'
            else:
                tg_class = 'tg-0lax'
            if client['status'] == 'Offline' and client['vlan'] == table_id:
                client_dict = {
                    "client_description": client['description'],
                    "client_mac": client['mac'],
                    "client_ip": client['ip']
                }
                list_of_clients.append(client_dict)
                temp_string = f'''
                    <tbody>
                    <tr>
                    <td class="{tg_class}">{client_dict["client_description"]}</td>
                    <td class="{tg_class}"><pre>{client_dict["client_mac"]}</pre></td>
                    <td class="{tg_class}"><pre>{client_dict["client_ip"]}</pre></td>
                    </tr>
                '''
                table_body_string += temp_string
                counter += 1
    number_of_clients = len(list_of_clients)
    html_string = f'''
        <style type="text/css">
            body {{
                background-color: #333;
                color:#fff;
                }}

            span {{
                border:1px solid #fff;
                padding:5px 15px;
                background:#444;
                }}

            th,td {{
                border:1px solid #aaa;
            }}

            .tg  {{
                border-collapse:collapse;
                border-spacing:0;
                }}

            .tg td {{
                font-family:Arial, sans-serif;
                font-size:14px;
                overflow:hidden;
                padding:10px 50px;
                word-break:normal;
                }}

            .tg th {{
                font-family:Arial, sans-serif;
                font-size:14px;
                font-weight:bold;
                text-transform:uppercase;
                overflow:hidden;
                padding:10px 5px;
                word-break:normal;
                text-align:center;
                background-color:#555;
                }}

            .tg .tg-alz1 {{
                background-color:#444;
                color:#fff;
                vertical-align:top
                }}

            .tg .tg-0lax {{
                background-color:#333;
                color:#fff;
                vertical-align:top
                }}
        </style>

        <center>
        <div>
        <h1>Table {str(table_id)[2:]} - VLAN {table_id} - {number_of_clients} client(s)</h1>
        <h2><pre>Current Option: <span>{dhcp_option}</span></pre></h2>
        </div>

        <table class="tg">
        <thead>
        <tr>
            <th>Model</th>
            <th>MAC Address</th>
            <th>IP Address</th>
        </tr>
        </thead>   
    '''
    html_string += table_body_string
    html_string += table_body_close

    f = open(f"table{str(table_id)[2:]}.html", "w")
    f.write(html_string)
    f.close()


if __name__ == '__main__':
    main()