from flask import Flask, render_template
import requests
import creds


API_KEY = creds.creds['api_key']
API_HEADERS = {'X-Cisco-Meraki-API-Key': API_KEY,
               'Accept': '*/*'}
base_url = 'https://api.meraki.com/api/v0/'
lab_network = 'L_613052499275810377'


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/7')
def seven():
    with app.app_context():
        return render_template('table_template.html',
                               clients=get_clients(),
                               table=7,
                               vlan=107,
                               num_clients=len(get_clients()),
                               vlan_option=get_vlan_options())


def get_clients():
    table = 107
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
    table = 107
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
    app.run(debug=True)
