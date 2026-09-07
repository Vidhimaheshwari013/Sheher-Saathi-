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
                    timeout=30,
                )

                if response.status_code != 200:
                    st.error(
                        f"Could not submit complaint. "
                        f"Status: {response.status_code}"
                    )
                    return

                complaint_data = response.json()

                # Save complaint ID for follow-up
                st.session_state["complaint_id"] = complaint_data["id"]

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

                    if isinstance(analysis, dict) and analysis.get("issues"):
                        for issue in analysis["issues"]:
                            st.write("### 🏷️ Issue")

                            st.write(
                                "**Category:**",
                                issue.get("category", "Not available"),
                            )

                            st.write(
                                "**📍 Location:**",
                                issue.get("location", "Not available"),
                            )

                            st.write(
                                "**👥 Affected group:**",
                                issue.get(
                                    "affected_group",
                                    "Not available",
                                ),
                            )

                            st.write(
                                "**⚠️ Severity:**",
                                f"{issue.get('severity', 'Not available')}/5",
                            )

                            st.write(
                                "**⏱️ Duration:**",
                                issue.get(
                                    "duration",
                                    "Not available",
                                ),
                            )

                        st.write(
                            "**🌐 Language:**",
                            analysis.get(
                                "language",
                                "Not available",
                            ),
                        )

                        # 3. Show follow-up question
                        if analysis.get("needs_followup"):
                            question = analysis.get(
                                "followup_question"
                            )

                            if question:
                                st.subheader("❓ We need a little more information")

                                st.info(question)

                                followup_answer = st.text_area(
                                    "Your answer",
                                    placeholder=(
                                        "Example: It happens every time "
                                        "it rains and students have to "
                                        "walk through the water."
                                    ),
                                    key="followup_answer",
                                )

                                if st.button(
                                    "Send Follow-up",
                                    type="primary",
                                ):
                                    if not followup_answer.strip():
                                        st.warning(
                                            "Please provide an answer."
                                        )
                                    else:
                                        complaint_id = st.session_state[
                                            "complaint_id"
                                        ]

                                        with st.spinner(
                                            "Updating your complaint... 🤖"
                                        ):
                                            followup_response = requests.post(
                                                f"{API_URL}/complaints/"
                                                f"{complaint_id}/followup",
                                                json={
                                                    "answer": (
                                                        followup_answer.strip()
                                                    )
                                                },
                                                timeout=30,
                                            )

                                        if followup_response.status_code == 200:
                                            updated = (
                                                followup_response.json()
                                            )

                                            st.success(
                                                "Complaint updated successfully! ✅"
                                            )

                                            st.write(
                                                "**Updated severity:**",
                                                f"{updated['severity']}/5",
                                            )

                                            st.write(
                                                "**Updated duration:**",
                                                updated["duration"],
                                            )

                                            st.write(
                                                "**Updated location:**",
                                                updated["location"],
                                            )

                                        else:
                                            st.error(
                                                "Could not update the "
                                                "complaint. "
                                                f"Status: "
                                                f"{followup_response.status_code}"
                                            )

                    else:
                        st.write(analysis)

                else:
                    st.warning(
                        "Complaint was submitted, but AI analysis "
                        "could not be completed. "
                        f"Status: {analysis_response.status_code}"
                    )

            except requests.exceptions.RequestException:
                st.error(
                    "Could not connect to the Sheher Saathi backend. "
                    "Make sure the FastAPI server is running."
                )
                