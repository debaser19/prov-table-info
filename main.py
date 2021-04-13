import meraki
import pandas as pd
import streamlit as st
import auth

#TODO: need to move layout to new function
def get_dhcp_option(dashboard, vlan):
    vlans = dashboard.appliance.getNetworkApplianceVlans(auth.buf_lab_network)
    dhcp_option = 'UNSET'
    for v in vlans:
        if v['id'] == vlan and 'dhcpOptions' in v:
            for option in v['dhcpOptions']:
                dhcp_option = option['value']
    
    dhcp_text = st.text_input(f'Table {vlan}', dhcp_option)
    
    #TODO: need to change this to a 2 col layout
    if dhcp_text and dhcp_text != 'UNSET':
        new_dhcp_option = [
            {
                'code': 66,
                'type': 'text',
                'value': dhcp_text
            }
        ]
        dashboard.appliance.updateNetworkApplianceVlan(auth.buf_lab_network, vlan, dhcpOptions=new_dhcp_option)
        st.write(f'Table {vlan} has been set to {dhcp_text}')
    else:
        dashboard.appliance.updateNetworkApplianceVlan(auth.buf_lab_network, vlan, dhcpOptions=[])
        st.write(f'Table {vlan} has been unset')


def get_clients(dashboard, net):
       
    return dashboard.networks.getNetworkClients(net, -1)


def list_clients(dashboard, vlan):    
    clients = [c for c in get_clients(dashboard, auth.buf_lab_network) if c['vlan'] == vlan and c['status'] == 'Online']
    client_df = pd.DataFrame.from_records(clients)
    
    try:
        st.dataframe(client_df[['mac', 'description', 'ip']])
    except Exception:
        st.write('No clients currently online')


def main():
    # define dashboard
    dashboard = meraki.DashboardAPI(auth.api_key, suppress_logging=True)

    # get buf clients
    table = st.selectbox(
        'Select a table',
        (list(range(101,109)))
    )
    get_dhcp_option(dashboard, table)
    list_clients(dashboard, table)


if __name__ == '__main__':
    main()