import creds
import requests
from flask import render_template
import flask
import sys
import time


API_KEY = creds.creds['api_key']
API_HEADERS = {'X-Cisco-Meraki-API-Key': API_KEY,
               'Accept': '*/*'}
base_url = 'https://api.meraki.com/api/v0/'
lab_network = 'L_613052499275810377'

app = flask.Flask('prov info')


def get_clients():
    r = requests.get(base_url+'networks/'+lab_network+'/clients?perPage=1000', headers=API_HEADERS)
    clients = r.json()

    client_list = []
    for client in clients:
        if client['status'] == 'Online' and client['vlan'] == int(table):
            client_dict = {'vlan': client['vlan'],
                           'client': client['description'],
                           'mac': client['mac'],
                           'ip': client['ip']}

            client_list.append(client_dict)

    return client_list


def get_vlan_options():
    r = requests.get(base_url + 'networks/' + lab_network + '/vlans', headers=API_HEADERS)
    vlans = r.json()

    for vlan in vlans:
        # vlan_option = 'UNSET'
        if vlan['id'] == int(table):
            if vlan['dhcpOptions']:
                # vlan_option = vlan['dhcpOptions'][0]['value']
                vlan_option = vlan['dhcpOptions'][0]['value']
            else:
                vlan_option = 'UNSET'

            # vlan_dict = {'vlan': vlan['id'],
            #              'option': vlan_option}

            return vlan_option


if __name__ == '__main__':
    while True:
        table = ''
        try:
            table = sys.argv[1]
        except IndexError:
            print('incorrect args - must pass in table in range 101 through 109')
            print('usage - python3 main.py 104')
            sys.exit(1)
        with app.app_context():
            rendered = render_template('table_template.html',
                                       clients=get_clients(),
                                       table=table[2:],
                                       vlan=table,
                                       num_clients=len(get_clients()),
                                       vlan_option=get_vlan_options())

            html_file = open(f'table{table[2:]}.html', 'w')
            html_file.write(rendered)
            html_file.close()

            for client in get_clients():
                print(f'Client: {client["client"]}')
                print(f'MAC: {client["mac"]}')
                print(f'IP: {client["ip"]}')
                print('')

            print('Sleeping for 5 seconds...')
            time.sleep(5)
            print('Getting list of clients...')
