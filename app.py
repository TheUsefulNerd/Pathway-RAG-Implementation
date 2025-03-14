import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Finance RAG System", layout="wide")

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "News"],
        icons=["house", "newspaper"],
        menu_icon="cast",
        default_index=0
    )

# Load pages dynamically
if selected == "Home":
    from Home import show_home
    show_home()
elif selected == "News":
    from News import show_news
    show_news()