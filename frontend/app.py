import streamlit as st

from views.citizen import show_citizen_page
from views.admin import show_admin_page


st.set_page_config(
    page_title="Sheher Saathi",
    page_icon="🏙️",
    layout="wide",
)

st.title("🏙️ Sheher Saathi")
st.write("Your civic issue intelligence platform")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Citizen Complaint",
        "Admin Dashboard",
    ],
)

if page == "Citizen Complaint":
    show_citizen_page()

elif page == "Admin Dashboard":
    show_admin_page()

