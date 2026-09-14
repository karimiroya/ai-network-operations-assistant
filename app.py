import streamlit as st
import pandas as pd
import requests

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
    Telecom network monitoring and AI-assisted analysis
    for simulated network nodes using Python, Pandas,
    NumPy and a hosted LLM.
    """
)


# --------------------------------
# Load network data
# --------------------------------

@st.cache_data
def load_network_data():

    return pd.read_csv(
        DATA_PATH
    )


# --------------------------------
# AI assessment
# --------------------------------

def generate_ai_assessment(
    node_id,
    location,
    latency,
    packet_loss,
    cpu_usage,
    analysis
):

    api_key = st.secrets.get(
        "OPENROUTER_API_KEY",
        None
    )

    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is not configured."
        )

    prompt = f"""
You are an AI Network Operations Assistant.

Analyze the following simulated telecom network node.

Node ID: {node_id}
Location: {location}

Network metrics:
- Latency: {latency} ms
- Packet loss: {packet_loss}%
- CPU usage: {cpu_usage}%

Automated severity analysis:
{analysis}

Your task:

1. Explain whether the node has a network problem.
2. Identify which metrics are concerning.
3. Explain the severity.
4. Recommend what a network operations engineer should investigate.

Rules:
- Use only the provided measurements.
- Do not invent network data.
- Be concise.
- Give a clear operational explanation.
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data[
        "choices"
    ][0][
        "message"
    ][
        "content"
    ]


# --------------------------------
# Load data
# --------------------------------

df = load_network_data()


node_ids = df[
    "node_id"
].tolist()


selected_node = st.selectbox(
    "Select Network Node",
    node_ids
)


node = df[
    df["node_id"] == selected_node
].iloc[0]


# --------------------------------
# Network metrics
# --------------------------------

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


# --------------------------------
# Automated severity analysis
# --------------------------------

analysis = analyze_metrics(
    latency_ms=node["latency_ms"],
    packet_loss=node["packet_loss"],
    cpu_usage=node["cpu_usage"]
)


st.subheader(
    "🚨 Automated Network Analysis"
)


severity = str(
    analysis.get(
        "severity",
        "unknown"
    )
)


score = analysis.get(
    "total_score",
    analysis.get(
        "score",
        "N/A"
    )
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


with st.expander(
    "View detailed scoring"
):

    st.json(
        analysis
    )


st.divider()


# --------------------------------
# AI network assessment
# --------------------------------

st.subheader(
    "🤖 AI Network Assessment"
)


st.write(
    """
    Generate an AI explanation of the current node's
    network condition and recommended investigation steps.
    """
)


if st.button(
    "Generate AI Analysis",
    type="primary"
):

    with st.spinner(
        "AI is analyzing the network..."
    ):

        try:

            ai_answer = generate_ai_assessment(
                node_id=selected_node,
                location=node["location"],
                latency=node["latency_ms"],
                packet_loss=node["packet_loss"],
                cpu_usage=node["cpu_usage"],
                analysis=analysis
            )


            st.success(
                "AI analysis complete"
            )


            st.markdown(
                ai_answer
            )


        except requests.HTTPError as error:

            st.error(
                f"OpenRouter API error: {error}"
            )


        except requests.RequestException as error:

            st.error(
                f"Network error: {error}"
            )


        except Exception as error:

            st.error(
                f"AI analysis failed: {error}"
            )