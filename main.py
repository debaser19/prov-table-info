import meraki
import pandas as pd
import streamlit as st
import auth

#TODO: need to move layout to new function
def get_dhcp_option(dashboard, warehouse, vlan):
    vlans = dashboard.appliance.getNetworkApplianceVlans(warehouse)
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
        dashboard.appliance.updateNetworkApplianceVlan(warehouse, vlan, dhcpOptions=new_dhcp_option)
        st.write(f'Table {vlan} has been set to {dhcp_text}')
    else:
        dashboard.appliance.updateNetworkApplianceVlan(warehouse, vlan, dhcpOptions=[])
        st.write(f'Table {vlan} has been unset')


def get_clients(dashboard, warehouse):
       
    return dashboard.networks.getNetworkClients(warehouse, -1)


def list_clients(dashboard, warehouse, vlan):    
    clients = [c for c in get_clients(dashboard, warehouse) if c['vlan'] == vlan and c['status'] == 'Online']
    client_df = pd.DataFrame.from_records(clients)
    
    try:
        st.dataframe(client_df[['mac', 'description', 'ip']])
    except Exception:
        st.write('No clients currently online')


def main():
    # define dashboard
    dashboard = meraki.DashboardAPI(auth.api_key, suppress_logging=True)

    # Warehouse selector
    warehouse = st.sidebar.selectbox(
        'Select a Warehouse',
        ['BUF', 'RNO']
    )

    if warehouse == 'BUF':
        warehouse = auth.buf_lab_network
        table = st.sidebar.selectbox(
            'Select a table',
            (list(range(101,109)))
        )
    else:
        warehouse = auth.rno_lab_network
        table = st.sidebar.selectbox(
            'Select a table',
            (list(range(201,208)))
        )

    # get buf clients
    get_dhcp_option(dashboard, warehouse, table)
    list_clients(dashboard, warehouse, table)


if __name__ == '__main__':
    main()