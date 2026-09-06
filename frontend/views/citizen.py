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

    location = st.text_input(
        "📍 Location",
        placeholder="Example: Rajpur Road, Dehradun",
    )

    if st.button("Submit Complaint", type="primary"):
        if not complaint.strip():
            st.warning("Please describe your issue.")
        elif not location.strip():
            st.warning("Please enter the location.")
        else:
            st.success("Complaint received!")
            st.write("**Issue:**", complaint)
            st.write("**Location:**", location)
            