import streamlit as st

st.set_page_config(
    page_title="Sheher Saathi",
    page_icon="🏙️",
    layout="wide"
)

st.title("🏙️ Sheher Saathi")
st.write("Your civic issue intelligence platform")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Citizen Complaint",
        "Admin Dashboard"
    ]
)

if page == "Citizen Complaint":
    st.header("📝 Citizen Complaint")
    st.write("Report a civic issue in your area.")

    complaint = st.text_area(
        "Describe your issue",
        placeholder="Example: Bhai school ke bahar baarish ke baad pura road paani se bhar jaata hai..."
    )

    if st.button("Submit Complaint"):
        if complaint.strip():
            st.success("Complaint received!")
        else:
            st.warning("Please describe your issue.")

elif page == "Admin Dashboard":
    st.header("📊 Admin Dashboard")
    st.write("Civic issue dashboard will appear here.")