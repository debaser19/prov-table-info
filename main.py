""" Super rad script to display provisioning table DHCP Options

Author: Steve Stoveld
Created: 7/18/2020
Modified: 7/18/2020
"""

import requests
import json
import creds

# set api keys and api request urls
apikey = creds.creds['api_key']
vlans_url = creds.creds['vlan_net']
clients_url = creds.creds['clients_net']

# hit the api with get request and store the json response in a variable
response = requests.get(vlans_url, headers={"X-Cisco-Meraki-API-Key":apikey})
tables = response.json()
response = requests.get(clients_url, headers={"X-Cisco-Meraki-API-Key":apikey})
clients = response.json()

# create empty list to append the table dicts to
list_of_tables = []

# loop through each table
for table in tables:
    # create empty list for each table to append the client dicts to
    list_of_clients = []
    table_option = ''
    # only check tables 1 through 9
    if table['id'] in range(101,110):
        # make sure dhcpOptions is in the data
        if 'dhcpOptions' in table:
            # create the table dict to be appended to the list
            # empty clients list will have the client dicts appended to it
            for option in table['dhcpOptions']:
                if option['value'] != '':
                    table_option = option['value']
                else:
                    table_option = ''
            table_dict = {"table":table['id'], "option":table_option, "clients":list_of_clients}
        # loop through all the clients on the current table
        for client in clients:
            # make sure the client is on the same vlan as the table
            if client['vlan'] == table['id']:
                # create the client dict and append it to the list of client dicts
                client_dict = {"description":client['description'], "ip":client['ip'], "mac":client['mac']}
                list_of_clients.append(client_dict)
        # append the tables dict with list of clients dicts to the list of tables dict
        list_of_tables.append(table_dict)

# loop through the tables and print them out with clients
for table in list_of_tables:
    print(json.dumps(table, indent=3))