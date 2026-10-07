import streamlit as st


def secret(name, default=None):
    # st.secrets raises when no secrets.toml exists; the app must still run then
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default
