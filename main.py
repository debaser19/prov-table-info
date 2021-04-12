import meraki
import pandas as pd
import streamlit as st
import auth


def get_clients(dashboard, net):
       
    return dashboard.clients.getNetworkClients(net,-1)


def list_clients(dashboard, vlan):    
    clients = [c for c in get_clients(dashboard, auth.buf_lab_network) if c['vlan'] == vlan and c['status'] == 'Online']
    client_df = pd.DataFrame.from_records(clients)
    
    st.dataframe(client_df[['mac', 'description', 'ip']])


def main():
    # define dashboard
    dashboard = meraki.DashboardAPI(auth.api_key, suppress_logging=True)

    # get buf clients
    list_clients(dashboard, 90)


if __name__ == '__main__':
    main()