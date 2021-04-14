import CloudFlare
import streamlit as st
import auth


def main():
    st.title('CloudCoFlare')
    st.write('DNS Updater app for CloudCo')
    st.write('Select the record type, enter the subdomain and ip address. Press enter when done to confirm.')

    zone_name = 'cloudcopartner.com'
    cf = CloudFlare.CloudFlare(email=auth.cf_email, token=auth.cf_api_key)

    # query the zone name and expect only one value back
    try:
        zones = cf.zones.get(params={'name': zone_name, 'per_page': 1})
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones.get %d %s - api call failed' % (e, e))
    except Exception as e:
        exit('/zones.get - %s api call failed' % e)

    if len(zones) == 0:
        exit('No  zones found')

    # extract the zone_id which is needed to process that zone
    zone = zones[0]
    zone_id = zone['id']

    # request the DNS records from that zone
    try:
        dns_records = cf.zones.dns_records.get(zone_id)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones/dns_records.get %d %s - api call failed' % (e, e))

    record_type = st.selectbox(
        'Record Type',
        ['A', 'CNAME'])
    record_name = st.text_input('Record Subdomain (omit ".cloudcopartner.com")')
    record_content = st.text_input('IP Address')

    dns_record = {
        'type': record_type,
        'name': record_name,
        'content': record_content,
        'proxied': False
    }

    if record_name and record_content:
        try:
            r = cf.zones.dns_records.post(zone_id, data=dns_record)
            st.write('Record submitted successfully')
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            st.write('Record submission failed')
            exit('/zones.dns_records.post %s %s - %d %s' % (zone_name, dns_record['name'], e, e))

        dns_record = r
        st.write('\t%s %30s %6d %-5s %s ; proxied=%s proxiable=%s' % (
            dns_record['id'],
            dns_record['name'],
            dns_record['ttl'],
            dns_record['type'],
            dns_record['content'],
            dns_record['proxied'],
            dns_record['proxiable']
        ))


if __name__ == '__main__':
    main()