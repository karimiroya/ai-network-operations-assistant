import streamlit as st
import pandas as pd

from analyzer import analyze_metrics


DATA_PATH = "data/network_metrics.csv"


st.set_page_config(
    page_title="AI Network Operations Assistant",
    page_icon="📡",
    layout="wide"
)


st.title("📡 AI Network Operations Assistant")

st.write(
    """
    Telecom network monitoring dashboard for simulated network nodes,
    using Python, Pandas, NumPy and automated severity analysis.
    """
)


@st.cache_data
def load_network_data():
    return pd.read_csv(DATA_PATH)


df = load_network_data()


node_ids = df["node_id"].tolist()

selected_node = st.selectbox(
    "Select Network Node",
    node_ids
)


node = df[
    df["node_id"] == selected_node
].iloc[0]


st.subheader(
    f"📊 Network Metrics — {selected_node}"
)


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Latency",
        f"{node['latency_ms']} ms"
    )


with col2:
    st.metric(
        "Packet Loss",
        f"{node['packet_loss']}%"
    )


with col3:
    st.metric(
        "CPU Usage",
        f"{node['cpu_usage']}%"
    )


st.write(
    f"**Location:** {node['location']}"
)


analysis = analyze_metrics(
    latency_ms=node["latency_ms"],
    packet_loss=node["packet_loss"],
    cpu_usage=node["cpu_usage"]
)


st.subheader(
    "🚨 Automated Network Analysis"
)


severity = str(
    analysis.get("severity", "unknown")
)

score = analysis.get(
    "total_score",
    analysis.get("score", "N/A")
)


if severity.lower() == "critical":

    st.error(
        f"🔴 CRITICAL — Risk Score: {score}"
    )

elif severity.lower() in [
    "warning",
    "moderate"
]:

    st.warning(
        f"🟠 {severity.upper()} — Risk Score: {score}"
    )

else:

    st.success(
        f"🟢 {severity.upper()} — Risk Score: {score}"
    )


st.json(
    analysis
)


st.subheader(
    "🤖 Network Assessment"
)


if severity.lower() == "critical":

    st.markdown(
        f"""
Node **{selected_node}** in **{node['location']}**
is experiencing significant network degradation.

- **Latency:** {node['latency_ms']} ms
- **Packet Loss:** {node['packet_loss']}%
- **CPU Usage:** {node['cpu_usage']}%

The combined severity score indicates that
immediate investigation is recommended.
"""
    )

elif severity.lower() in [
    "warning",
    "moderate"
]:

    st.markdown(
        f"""
Node **{selected_node}** shows signs of degraded
network performance.

Further monitoring and investigation may be required.
"""
    )

else:

    st.markdown(
        f"""
Node **{selected_node}** is currently operating
within acceptable network conditions.
"""
    )