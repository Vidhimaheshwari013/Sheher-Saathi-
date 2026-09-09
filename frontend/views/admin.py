import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


def show_admin_page():
    st.header("📊 Admin Dashboard")
    st.caption(
        "Monitor emerging civic issues, connected complaints, "
        "and neighbourhood hotspots."
    )

    # =========================================================
    # FETCH DASHBOARD
    # =========================================================
    dashboard_data = {}

    try:
        dashboard_response = requests.get(
            f"{API_URL}/dashboard",
            timeout=10,
        )

        if dashboard_response.status_code == 200:
            dashboard_data = dashboard_response.json()

    except requests.exceptions.RequestException:
        st.error(
            "Could not connect to the Sheher Saathi backend. "
            "Make sure FastAPI is running."
        )
        return

    if not isinstance(dashboard_data, dict):
        dashboard_data = {}

    # =========================================================
    # FETCH CLUSTERS
    # =========================================================
    clusters_data = {}

    try:
        clusters_response = requests.get(
            f"{API_URL}/clusters",
            timeout=10,
        )

        if clusters_response.status_code == 200:
            clusters_data = clusters_response.json()

    except requests.exceptions.RequestException:
        clusters_data = {}

    # Extract clusters safely
    if isinstance(clusters_data, dict):
        clusters = clusters_data.get("clusters", [])
    elif isinstance(clusters_data, list):
        clusters = clusters_data
    else:
        clusters = []

    if not isinstance(clusters, list):
        clusters = []

    # =========================================================
    # FETCH CIVIC MEMORY
    # =========================================================
    memory_data = None
    memory_available = False

    try:
        memory_response = requests.get(
            f"{API_URL}/memory",
            timeout=10,
        )

        if memory_response.status_code == 200:
            memory_data = memory_response.json()
            memory_available = True

    except requests.exceptions.RequestException:
        memory_data = None

    # =========================================================
    # CIVIC PULSE
    # =========================================================
    st.subheader("🌆 Civic Pulse")
    st.caption("A quick view of what is happening across the city.")

    total_reports = dashboard_data.get(
        "total_reports",
        dashboard_data.get("total_complaints", 0),
    )

    connected_issues = len(clusters)

    high_priority = 0

    for cluster in clusters:
        if not isinstance(cluster, dict):
            continue

        priority = cluster.get("priority", {})

        if isinstance(priority, dict):
            level = str(
                priority.get("level", "")
            ).lower()

            if level == "high":
                high_priority += 1

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📋 Total Reports",
            total_reports,
        )

    with col2:
        st.metric(
            "🔗 Connected Issues",
            connected_issues,
        )

    with col3:
        st.metric(
            "⚠️ High Priority",
            high_priority,
        )

    st.divider()

    # =========================================================
    # CITY OVERVIEW
    # =========================================================
    st.subheader("🗺️ City Overview")

    city_col1, city_col2 = st.columns(2)

    with city_col1:
        st.write("**Total Complaints**")
        st.write(total_reports)

    with city_col2:
        verified_count = dashboard_data.get(
            "verified_count",
            dashboard_data.get("verified_complaints", 0),
        )

        st.write("**Verified Count**")
        st.write(verified_count)

    st.divider()

    # =========================================================
    # EMERGING CIVIC ISSUES
    # =========================================================
    st.subheader("🔥 Emerging Civic Issues")

    if not clusters:
        st.info(
            "No connected civic issues have been detected yet."
        )

    else:
        for index, cluster in enumerate(clusters):

            if not isinstance(cluster, dict):
                continue

            cluster_id = cluster.get(
                "cluster_id",
                index,
            )

            category = cluster.get(
                "category",
                "Civic issue",
            )

            locations = cluster.get(
                "locations",
                [],
            )

            complaint_ids = cluster.get(
                "complaint_ids",
                [],
            )

            priority = cluster.get(
                "priority",
                {},
            )

            # -------------------------------------------------
            # PRIORITY DATA
            # -------------------------------------------------
            priority_level = "Not available"
            priority_score = None
            average_severity = None
            report_count = len(complaint_ids)

            if isinstance(priority, dict):

                priority_level = priority.get(
                    "level",
                    "Not available",
                )

                priority_score = priority.get(
                    "score",
                    None,
                )

                average_severity = priority.get(
                    "avg_severity",
                    None,
                )

                report_count = priority.get(
                    "report_count",
                    report_count,
                )

            # -------------------------------------------------
            # ISSUE CARD
            # -------------------------------------------------
            with st.container(border=True):

                st.markdown(
                    f"### 🏷️ {str(category).title()}"
                )

                st.caption(
                    f"Connected issue #{cluster_id}"
                )

                info1, info2, info3 = st.columns(3)

                with info1:
                    st.write("**Reports**")
                    st.write(report_count)

                with info2:
                    st.write("**Priority**")
                    st.write(
                        str(priority_level).title()
                    )

                with info3:
                    st.write("**Severity**")

                    if average_severity is not None:
                        st.write(
                            f"{average_severity}/5"
                        )
                    else:
                        st.write("Not available")

                # -------------------------------------------------
                # LOCATIONS
                # -------------------------------------------------
                if isinstance(locations, list) and locations:

                    st.write("**📍 Locations**")

                    for location in locations:
                        st.write(
                            f"• {location}"
                        )

                elif locations:

                    st.write("**📍 Location**")
                    st.write(str(locations))

                # -------------------------------------------------
                # PRIORITY SCORE
                # -------------------------------------------------
                if priority_score is not None:
                    st.caption(
                        f"Priority score: {priority_score}"
                    )

                # -------------------------------------------------
                # COMPLAINT IDS
                # -------------------------------------------------
                if complaint_ids:

                    with st.expander(
                        "View connected complaint IDs"
                    ):
                        st.write(
                            ", ".join(
                                str(cid)
                                for cid in complaint_ids
                            )
                        )

    st.divider()

    # =========================================================
    # CIVIC MEMORY
    # =========================================================
    st.subheader("🧠 Civic Memory")

    st.caption(
        "Sheher Saathi uses previous civic reports "
        "to identify recurring problems and patterns."
    )

    if not memory_available:
        st.info(
            "Civic Memory is currently unavailable."
        )

    elif memory_data is None:
        st.info(
            "No Civic Memory data is available yet."
        )

    else:

        # -----------------------------------------------------
        # MEMORY AS A LIST
        # -----------------------------------------------------
        if isinstance(memory_data, list):

            if len(memory_data) == 0:
                st.info(
                    "No recurring civic patterns have been detected yet."
                )

            else:

                for item in memory_data:

                    if isinstance(item, dict):

                        title = (
                            item.get("category")
                            or item.get("title")
                            or item.get("issue")
                            or "Civic Pattern"
                        )

                        with st.container(border=True):

                            st.markdown(
                                f"### 🔁 {str(title).title()}"
                            )

                            for key, value in item.items():

                                if key in [
                                    "category",
                                    "title",
                                    "issue",
                                ]:
                                    continue

                                label = str(
                                    key
                                ).replace(
                                    "_",
                                    " ",
                                ).title()

                                if isinstance(value, list):

                                    if value:
                                        st.write(
                                            f"**{label}**"
                                        )

                                        for entry in value:
                                            st.write(
                                                f"• {entry}"
                                            )

                                elif isinstance(
                                    value,
                                    dict,
                                ):
                                    continue

                                elif value is not None:
                                    st.write(
                                        f"**{label}:** {value}"
                                    )

                    else:
                        st.write(str(item))

        # -----------------------------------------------------
        # MEMORY AS A DICTIONARY
        # -----------------------------------------------------
        elif isinstance(memory_data, dict):

            # Look for the common containers used by the API.
            memory_items = (
                memory_data.get("memory")
                or memory_data.get("memories")
                or memory_data.get("patterns")
                or memory_data.get("recurring_issues")
                or memory_data.get("data")
            )

            if isinstance(memory_items, list):

                if len(memory_items) == 0:
                    st.info(
                        "No recurring civic patterns have been detected yet."
                    )

                else:

                    for item in memory_items:

                        if isinstance(item, dict):

                            title = (
                                item.get("category")
                                or item.get("title")
                                or item.get("issue")
                                or "Recurring Civic Issue"
                            )

                            with st.container(border=True):

                                st.markdown(
                                    f"### 🔁 {str(title).title()}"
                                )

                                for key, value in item.items():

                                    if key in [
                                        "category",
                                        "title",
                                        "issue",
                                    ]:
                                        continue

                                    label = str(
                                        key
                                    ).replace(
                                        "_",
                                        " ",
                                    ).title()

                                    if isinstance(value, list):

                                        if value:
                                            st.write(
                                                f"**{label}**"
                                            )

                                            for entry in value:
                                                st.write(
                                                    f"• {entry}"
                                                )

                                    elif isinstance(
                                        value,
                                        dict,
                                    ):
                                        continue

                                    elif value is not None:
                                        st.write(
                                            f"**{label}:** {value}"
                                        )

                        else:
                            st.write(str(item))

            else:

                # -------------------------------------------------
                # DISPLAY SIMPLE MEMORY FIELDS
                # WITHOUT SHOWING RAW JSON
                # -------------------------------------------------
                displayed_anything = False

                for key, value in memory_data.items():

                    if value is None:
                        continue

                    label = str(
                        key
                    ).replace(
                        "_",
                        " ",
                    ).title()

                    if isinstance(value, list):

                        if not value:
                            continue

                        displayed_anything = True

                        st.write(
                            f"**{label}**"
                        )

                        for item in value:
                            if isinstance(item, dict):

                                with st.container(
                                    border=True
                                ):
                                    for sub_key, sub_value in item.items():

                                        sub_label = str(
                                            sub_key
                                        ).replace(
                                            "_",
                                            " ",
                                        ).title()

                                        if isinstance(
                                            sub_value,
                                            list,
                                        ):
                                            st.write(
                                                f"**{sub_label}**"
                                            )

                                            for entry in sub_value:
                                                st.write(
                                                    f"• {entry}"
                                                )

                                        elif sub_value is not None:
                                            st.write(
                                                f"**{sub_label}:** "
                                                f"{sub_value}"
                                            )

                            elif isinstance(
                                item,
                                str,
                            ):
                                st.write(
                                    f"• {item}"
                                )

                            else:
                                st.write(
                                    f"• {item}"
                                )

                    elif isinstance(
                        value,
                        dict,
                    ):
                        continue

                    else:
                        displayed_anything = True

                        st.write(
                            f"**{label}:** {value}"
                        )

                if not displayed_anything:
                    st.info(
                        "No recurring civic patterns have been detected yet."
                    )

        # -----------------------------------------------------
        # UNEXPECTED RESPONSE
        # -----------------------------------------------------
        else:
            st.info(
                "No recurring civic patterns have been detected yet."
            )
                    