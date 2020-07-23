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

    list_of_clients = []

    html_string = '''
        <center>
        <h1>Table X - VLAN X</h1>
        <h3>Current Option: http://example.option/company</h3>

        <style type="text/css">
            .tg  {border-collapse:collapse;border-color:#93a1a1;border-spacing:0;}
            .tg td{background-color:#fdf6e3;border-color:#93a1a1;border-style:solid;border-width:1px;color:#002b36;
            font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 50px;word-break:normal;}
            .tg th{background-color:#657b83;border-color:#93a1a1;border-style:solid;border-width:1px;color:#fdf6e3;
            font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;text-align:center;}
            .tg .tg-alz1{background-color:#eee8d5;text-align:left;vertical-align:top}
            .tg .tg-0lax{text-align:left;vertical-align:top}
        </style>
        <table class="tg">
        <thead>
        <tr>
            <th class="tg-0lax">Model</th>
            <th class="tg-0lax">MAC</th>
            <th class="tg-0lax">IP</th>
        </tr>
        </thead>   
    '''
    table_body_string = ''
    table_body_close = '''
        </tbody>
        </table>
        </center>
    '''

    try:
        # Get list of clients on network, filtering on timespan of last 14 days
        clients = dashboard.networks.getNetworkClients(network, timespan=60*60*24*14, perPage=1000, total_pages='all')
        # clients = json.dumps(clients)
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
            if client['status'] == 'Offline' and client['vlan'] in range(101,110) and counter <= 20:
                # print(json.dumps(client, indent=3))
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
                    <td class="{tg_class}">{client_dict["client_mac"]}</td>
                    <td class="{tg_class}">{client_dict["client_ip"]}</td>
                    </tr>
                '''
                table_body_string += temp_string
                counter += 1

    html_string += table_body_string
    html_string += table_body_close

    print(html_string)

    # print(list_of_clients)


    f = open("tableX.html", "w")
    f.write(html_string)
    f.close()


if __name__ == '__main__':
    main()