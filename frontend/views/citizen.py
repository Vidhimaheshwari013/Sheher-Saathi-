import streamlit as st


def show_citizen_page():
    st.header("📝 Citizen Complaint")
    st.write("Report a civic issue in your area.")

    complaint = st.text_area(
        "Describe your issue",
        placeholder=(
            "Example: Bhai school ke bahar baarish ke baad "
            "pura road paani se bhar jaata hai..."
        ),
        height=150,
    )

    if st.button("Submit Complaint", type="primary"):
        if complaint.strip():
            st.success("Complaint received!")
        else:
            st.warning("Please describe your issue.")