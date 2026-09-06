import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


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
            st.warning("Please describe the issue.")

        elif not location.strip():
            st.warning("Please enter the location.")

        else:
            raw_text = (
                f"{complaint.strip()} "
                f"Location: {location.strip()}"
            )

            try:
                # 1. Create complaint
                response = requests.post(
                    f"{API_URL}/complaints",
                    json={"raw_text": raw_text},
                    timeout=10,
                )

                if response.status_code != 200:
                    st.error(
                        f"Could not submit complaint. "
                        f"Status: {response.status_code}"
                    )
                    return

                complaint_data = response.json()

                st.success("Complaint submitted successfully! ✅")

                st.write("**Complaint ID:**", complaint_data["id"])
                st.write("**Status:**", complaint_data["status"])

                # 2. Analyze complaint using AI
                with st.spinner("Analyzing your complaint... 🤖"):
                    analysis_response = requests.post(
                        f"{API_URL}/complaints/analyze",
                        json={"raw_text": raw_text},
                        timeout=30,
                    )

                if analysis_response.status_code == 200:
                    analysis = analysis_response.json()

                    st.subheader("🤖 AI Analysis")
                    st.write(analysis)

                else:
                    st.warning(
                        "Complaint was submitted, but AI analysis "
                        f"could not be completed. "
                        f"Status: {analysis_response.status_code}"
                    )

            except requests.exceptions.RequestException:
                st.error(
                    "Could not connect to the Sheher Saathi backend. "
                    "Make sure the FastAPI server is running."
                )