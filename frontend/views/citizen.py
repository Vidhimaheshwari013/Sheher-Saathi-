import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


# ============================================================
# SESSION STATE
# ============================================================

def init_state():

    if "citizen_page" not in st.session_state:
        st.session_state["citizen_page"] = "home"

    if "complaint_id" not in st.session_state:
        st.session_state["complaint_id"] = None

    if "complaints" not in st.session_state:
        st.session_state["complaints"] = []

    if "latest_analysis" not in st.session_state:
        st.session_state["latest_analysis"] = None


# ============================================================
# HEADER
# ============================================================

def render_header():

    title_col, nav_col = st.columns([2, 3])

    with title_col:

        st.title("🏙️ Sheher Saathi")

        st.caption(
            "Your city. Your voice. Your Saathi."
        )

    with nav_col:

        nav1, nav2, nav3 = st.columns(3)

        with nav1:

            if st.button(
                "Home",
                use_container_width=True
            ):

                st.session_state["citizen_page"] = "home"
                st.rerun()

        with nav2:

            if st.button(
                "Report Issue",
                use_container_width=True
            ):

                st.session_state["citizen_page"] = "report"
                st.rerun()

        with nav3:

            if st.button(
                "My Reports",
                use_container_width=True
            ):

                st.session_state["citizen_page"] = "reports"
                st.rerun()

    st.divider()


# ============================================================
# HOME PAGE
# ============================================================

def render_home():

    st.success(
        "🌱 Community Powered Governance"
    )

    st.header(
        "Something happening in your neighbourhood?"
    )

    st.write(
        "Tell Sheher Saathi about it. Describe the problem "
        "in your own words and we'll help connect it to "
        "what's happening across the city."
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "📝 Report an Issue",
            type="primary",
            use_container_width=True
        ):

            st.session_state["citizen_page"] = "report"
            st.rerun()

        st.caption(
            "Takes less than a minute"
        )

    with col2:

        if st.button(
            "📊 See What's Happening",
            use_container_width=True
        ):

            st.session_state["citizen_page"] = "reports"
            st.rerun()

    st.divider()

    st.subheader(
        "How Sheher Saathi works"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.subheader("🗣️ REPORT")

        st.write(
            "Describe a civic problem naturally in "
            "your own words."
        )

        st.caption(
            "English, Hindi or Hinglish are welcome."
        )

    with c2:

        st.subheader("🔗 CONNECT")

        st.write(
            "AI helps understand the complaint and "
            "identify connections between similar reports."
        )

    with c3:

        st.subheader("💡 UNDERSTAND")

        st.write(
            "Connected signals help reveal recurring "
            "issues affecting neighbourhoods and communities."
        )

    st.divider()

    st.info(
        "AI assists understanding. Humans remain in control."
    )


# ============================================================
# REPORT PAGE
# ============================================================

def render_report():

    st.header(
        "📝 Report an Issue"
    )

    st.write(
        "Tell us what is happening. You don't need to know "
        "the official category — just describe it naturally."
    )

    complaint = st.text_area(
        "What is happening?",
        placeholder=(
            "Example: Bhai school ke bahar baarish ke baad "
            "pura road paani se bhar jaata hai..."
        ),
        height=170
    )

    location = st.text_input(
        "📍 Where is this happening?",
        placeholder="Example: Rajpur Road, Dehradun"
    )

    st.caption(
        "💡 You can write in English, हिन्दी, or Hinglish."
    )

    if st.button(
        "Submit Complaint →",
        type="primary",
        use_container_width=True
    ):

        if not complaint.strip():

            st.warning(
                "Please describe the issue."
            )

        elif not location.strip():

            st.warning(
                "Please enter the location."
            )

        else:

            submit_complaint(
                complaint.strip(),
                location.strip()
            )

    st.write("")

    if st.button(
        "← Back to Home"
    ):

        st.session_state["citizen_page"] = "home"
        st.rerun()


# ============================================================
# SUBMIT COMPLAINT
# ============================================================

def submit_complaint(
    complaint,
    location
):

    raw_text = (
        f"{complaint} Location: {location}"
    )

    try:

        # ----------------------------------------------------
        # CREATE COMPLAINT
        # ----------------------------------------------------

        with st.spinner(
            "Submitting your complaint..."
        ):

            response = requests.post(
                f"{API_URL}/complaints",
                json={
                    "raw_text": raw_text
                },
                timeout=30
            )

        if response.status_code != 200:

            st.error(
                "Could not submit complaint. "
                f"Status: {response.status_code}"
            )

            return

        complaint_data = response.json()

        complaint_id = complaint_data["id"]

        st.session_state["complaint_id"] = complaint_id

        # ----------------------------------------------------
        # SAVE COMPLAINT FOR MY REPORTS
        # ----------------------------------------------------

        st.session_state["complaints"].append(
            {
                "id": complaint_id,
                "raw_text": raw_text,
                "status": complaint_data.get(
                    "status",
                    "Submitted"
                )
            }
        )

        st.success(
            "Complaint submitted successfully! ✅"
        )

        st.info(
            f"Your Complaint ID is #{complaint_id}"
        )

        # ----------------------------------------------------
        # AI ANALYSIS
        # ----------------------------------------------------

        with st.spinner(
            "Sheher Saathi is understanding your complaint... 🤖"
        ):

            analysis_response = requests.post(
                f"{API_URL}/complaints/analyze",
                json={
                    "raw_text": raw_text
                },
                timeout=30
            )

        if analysis_response.status_code == 200:

            analysis = analysis_response.json()

            st.session_state["latest_analysis"] = analysis

            render_analysis(
                analysis
            )

        else:

            st.warning(
                "Your complaint was submitted, but AI analysis "
                "could not be completed right now."
            )

            st.caption(
                f"Analysis status: "
                f"{analysis_response.status_code}"
            )

    except requests.exceptions.RequestException as error:

        st.error(
            "Could not connect to the Sheher Saathi backend."
        )

        st.caption(
            f"Connection error: {error}"
        )


# ============================================================
# AI ANALYSIS
# ============================================================

def render_analysis(
    analysis
):

    st.divider()

    st.header(
        "🤖 Sheher Saathi understood"
    )

    st.write(
        "Here's how your complaint was structured by the AI."
    )

    if not isinstance(
        analysis,
        dict
    ):

        st.write(
            analysis
        )

        return

    issues = analysis.get(
        "issues",
        []
    )

    if not issues:

        st.info(
            "No structured issue information was returned."
        )

        return

    # --------------------------------------------------------
    # DISPLAY EACH ISSUE
    # --------------------------------------------------------

    for index, issue in enumerate(
        issues
    ):

        st.subheader(
            f"🔎 AI Identified Issue {index + 1}"
        )

        category = issue.get(
            "category",
            "Civic issue"
        )

        st.markdown(
            f"### {str(category).title()}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "📍 Location"
            )

            st.write(
                issue.get(
                    "location",
                    "Not available"
                )
            )

            st.write(
                "👥 Affected group"
            )

            st.write(
                issue.get(
                    "affected_group",
                    "Not available"
                )
            )

            st.write(
                "⏱️ Duration"
            )

            st.write(
                issue.get(
                    "duration",
                    "Not available"
                )
            )

        with col2:

            severity = issue.get(
                "severity",
                "Not available"
            )

            st.write(
                "⚠️ Severity"
            )

            if severity != "Not available":

                st.write(
                    f"{severity}/5"
                )

            else:

                st.write(
                    "Not available"
                )

            st.write(
                "🌐 Language"
            )

            st.write(
                analysis.get(
                    "language",
                    "Not available"
                )
            )

        st.divider()

    # --------------------------------------------------------
    # FOLLOW-UP
    # --------------------------------------------------------

    if analysis.get(
        "needs_followup"
    ):

        question = analysis.get(
            "followup_question"
        )

        if question:

            st.subheader(
                "❓ One more thing"
            )

            st.info(
                question
            )

            followup_answer = st.text_area(
                "Your answer",
                placeholder=(
                    "Example: It happens every time it rains "
                    "and students have to walk through the water."
                ),
                key="followup_answer"
            )

            if st.button(
                "Send Follow-up →",
                type="primary",
                use_container_width=True
            ):

                if not followup_answer.strip():

                    st.warning(
                        "Please provide an answer."
                    )

                else:

                    submit_followup(
                        followup_answer.strip()
                    )


# ============================================================
# FOLLOW-UP API
# ============================================================

def submit_followup(
    answer
):

    complaint_id = st.session_state.get(
        "complaint_id"
    )

    if not complaint_id:

        st.error(
            "Complaint ID was not found."
        )

        return

    try:

        with st.spinner(
            "Updating your complaint... 🤖"
        ):

            response = requests.post(
                f"{API_URL}/complaints/"
                f"{complaint_id}/followup",
                json={
                    "answer": answer
                },
                timeout=30
            )

        if response.status_code == 200:

            updated = response.json()

            st.success(
                "Complaint updated successfully! ✅"
            )

            st.subheader(
                "Updated complaint"
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Severity",
                    f"{updated.get('severity', '-')}/5"
                )

            with c2:

                st.metric(
                    "Duration",
                    updated.get(
                        "duration",
                        "-"
                    )
                )

            with c3:

                st.metric(
                    "Location",
                    updated.get(
                        "location",
                        "-"
                    )
                )

        else:

            st.error(
                "Could not update the complaint. "
                f"Status: {response.status_code}"
            )

    except requests.exceptions.RequestException as error:

        st.error(
            "Could not connect to the backend."
        )

        st.caption(
            f"Connection error: {error}"
        )


# ============================================================
# MY REPORTS
# ============================================================

def render_reports():

    st.header(
        "📋 My Reports"
    )

    st.write(
        "Keep track of the complaints you've submitted "
        "in this session."
    )

    complaints = st.session_state.get(
        "complaints",
        []
    )

    if not complaints:

        st.info(
            "You haven't submitted any complaints "
            "in this session yet."
        )

        if st.button(
            "Report an Issue",
            type="primary"
        ):

            st.session_state["citizen_page"] = "report"
            st.rerun()

        return

    for complaint in reversed(
        complaints
    ):

        st.subheader(
            f"Complaint #{complaint['id']}"
        )

        st.write(
            complaint["raw_text"]
        )

        status = complaint.get(
            "status",
            "Submitted"
        )

        st.success(
            f"Status: {status}"
        )

        st.divider()

    if st.button(
        "← Back to Home"
    ):

        st.session_state["citizen_page"] = "home"
        st.rerun()


# ============================================================
# MAIN CITIZEN PAGE
# ============================================================

def show_citizen_page():

    init_state()

    render_header()

    page = st.session_state[
        "citizen_page"
    ]

    if page == "home":

        render_home()

    elif page == "report":

        render_report()

    elif page == "reports":

        render_reports()

    else:

        st.session_state["citizen_page"] = "home"
        st.rerun()
        