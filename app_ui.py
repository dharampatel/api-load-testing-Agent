# streamlit_app.py
import streamlit as st
import tempfile
import pandas as pd
import os
import time

from app.agents.load_test_graph import create_load_test_graph
from app.swagger.swagger_parser import parse_swagger

# ------------------- UI HEADER -------------------
st.set_page_config(page_title="🚀 API Load Tester", layout="wide")
st.title("🧠 API Load Testing Dashboard")

# ------------------- UPLOAD SWAGGER -------------------
st.header("📄 Upload Swagger File")
uploaded_file = st.file_uploader("Upload Swagger JSON", type=["json"])

load_graph = create_load_test_graph()

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        tmp.write(uploaded_file.read())
        swagger_path = tmp.name

    # Parse endpoints
    endpoints = parse_swagger(swagger_path)
    endpoint_list = [f"{ep['method']} {ep['path']}" for ep in endpoints]
    st.success(f"✅ Parsed {len(endpoint_list)} endpoints from Swagger.")

    # ------------------- BASE URL -------------------
    st.header("🌐 Target API Server")
    base_url = st.text_input(
        "Enter the Base URL of your API server",
        value="http://127.0.0.1:8000",
        placeholder="Example: http://localhost:8000"
    )

    # ------------------- SELECT ENDPOINTS -------------------
    st.header("🧩 Select Endpoints")
    selected_endpoints = st.multiselect(
        "Choose endpoints to test",
        endpoint_list,
        default=endpoint_list[:2]
    )

    # ------------------- TEST CONFIGURATION -------------------
    st.header("⚙️ Load Test Configuration")
    col1, col2, col3 = st.columns(3)
    with col1:
        users = st.number_input("Users", min_value=1, value=10)
    with col2:
        spawn_rate = st.number_input("Spawn Rate", min_value=1, value=2)
    with col3:
        run_time = st.text_input("Run Time (e.g., 10s, 1m)", value="10s")

    # ------------------- RUN LOAD TEST -------------------
    if st.button("🚀 Run Load Test"):
        if not base_url.strip():
            st.error("❌ Please enter a valid Base URL before running the test.")
        else:
            selected_indexes = [endpoint_list.index(e) for e in selected_endpoints]
            initial_state = {
                "swagger_path": swagger_path,
                "base_url": base_url,
                "users": users,
                "spawn_rate": spawn_rate,
                "run_time": run_time,
                "selected_indexes": selected_indexes,
            }

            st.subheader("🧩 Execution Progress")
            progress = st.progress(0)
            status_box = st.empty()
            log_area = st.empty()
            logs = []

            node_sequence = ["parse_swagger", "generate_payload", "run_locust", "summary"]
            total_nodes = len(node_sequence)
            current_node = 0
            final_state = {}

            for node_name, event in load_graph.stream(initial_state, stream_mode="events"):
                state = event.get("state", {})
                final_state = state

                # --- Node Status ---
                if "parse_swagger" in node_name:
                    status_box.info("📄 Parsing Swagger file...")
                elif "generate_payload" in node_name:
                    status_box.warning("🧠 Generating payloads...")
                elif "run_locust" in node_name:
                    status_box.warning("🚀 Running Locust load test...")
                elif "summary" in node_name:
                    status_box.success("📊 Summarizing results...")

                # --- Progress and Log ---
                current_node += 1
                progress.progress(min(current_node / total_nodes, 1.0))
                logs.append(f"[{node_name}] ✅ completed")
                log_area.code("\n".join(logs))
                time.sleep(0.5)  # slight delay for smooth progress animation

            # ✅ Done
            progress.progress(1.0)
            st.success("✅ Test Completed Successfully")

            # ------------------- SUMMARY SECTION -------------------
            st.markdown("### 📈 Test Summary")

            csv_path = None
            if isinstance(final_state, dict):
                csv_path = final_state.get("locust_result_csv")
            else:
                csv_path = getattr(final_state, "locust_result_csv", None)

            # Fallback known path
            if not csv_path or not os.path.exists(csv_path):
                alt_path = os.path.abspath("app/agents/loadtest_results/locust_result_stats.csv")
                if os.path.exists(alt_path):
                    csv_path = alt_path

            if csv_path and os.path.exists(csv_path):
                st.success(f"✅ Load test results found → {csv_path}")
                df = pd.read_csv(csv_path)

                # Normalize and match expected columns
                cols = [c.strip() for c in df.columns]
                lowcols = [c.lower().strip() for c in cols]

                candidates = {
                    "name": ["name", "request name", "endpoint", "type"],
                    "requests": ["request count", "# requests", "# reqs", "requests", "reqs"],
                    "fails": ["failure count", "# fails", "# failures", "failures"],
                    "avg": ["average response time", "avg", "average_response_time", "average response time (ms)"],
                }


                def find_col(possible):
                    for p in possible:
                        for orig, low in zip(cols, lowcols):
                            if p.lower() == low or p.lower() in low:
                                return orig
                    return None


                name_col = find_col(candidates["name"]) or "Name"
                req_col = find_col(candidates["requests"]) or "Request Count"
                fail_col = find_col(candidates["fails"]) or "Failure Count"
                avg_col = find_col(candidates["avg"]) or "Average Response Time"

                # Find Aggregated row
                try:
                    agg_row = df[df[name_col].astype(str).str.lower().eq("aggregated")]
                    if agg_row.empty:
                        agg_row = df.tail(1)
                    summary_row = agg_row.iloc[0]
                except Exception:
                    summary_row = df.tail(1).iloc[0]


                def to_int(x):
                    try:
                        return int(float(x))
                    except Exception:
                        return 0


                def to_float(x):
                    try:
                        return float(x)
                    except Exception:
                        return 0.0


                total_reqs = to_int(summary_row.get(req_col, 0))
                total_fails = to_int(summary_row.get(fail_col, 0))
                avg_time = to_float(summary_row.get(avg_col, 0.0))

                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("🧪 Total Requests", total_reqs)
                col2.metric("✅ Successful", total_reqs - total_fails)
                col3.metric("❌ Failed", total_fails)
                col4.metric("⚡ Avg Time (ms)", round(avg_time, 2))

                st.divider()
                st.markdown("### 📊 Detailed Performance Data")
                st.dataframe(df)

                # CSV download
                st.download_button(
                    label="⬇️ Download CSV Results",
                    data=open(csv_path, "rb").read(),
                    file_name="locust_results.csv",
                    mime="text/csv",
                )

            else:
                st.warning("⚠️ No Locust CSV found — check logs for errors.")

            # --- Raw Summary Text (if available) ---
            if "summary" in final_state:
                st.text_area("📝 Raw Summary", final_state["summary"], height=150)
