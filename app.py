import streamlit as st
import multiapp
from apps import home, prov, cloudcoflare
import auth

app = multiapp.MultiApp()

# Add all your application here
app.add_app("Home", home.main)
app.add_app("Prov", prov.main)
app.add_app("CloudCoFlare", cloudcoflare.main)

# The main app
app.run()