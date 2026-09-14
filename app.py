import streamlit as st
import requests

from agent import ask_agent


API_BASE_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Network Operations Assistant",
    page_icon="📡",
    layout="wide"
)


st.title("📡 AI Network Operations Assistant")

st.write(
    """
    Agentic AI assistant for monitoring and analyzing
    simulated telecom network nodes using LangChain,
    Qwen2.5, FastAPI, Pandas and NumPy.
    """
)


# --------------------------------
# Load network nodes
# --------------------------------

def get_nodes():

    response = requests.get(
        f"{API_BASE_URL}/network/nodes",
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def get_node_analysis(node_id):

    response = requests.get(
        f"{API_BASE_URL}/network/analyze/{node_id}",
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# --------------------------------
# Network dashboard
# --------------------------------

try:

    nodes = get_nodes()

    node_ids = [
        node["node_id"]
        for node in nodes
    ]

    selected_node = st.selectbox(
        "Select Network Node",
        node_ids
    )

    analysis = get_node_analysis(
        selected_node
    )

    metrics = analysis["metrics"]

    st.subheader(
        f"📊 Network Metrics — {selected_node}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Latency",
            f"{metrics['latency_ms']} ms"
        )

    with col2:
        st.metric(
            "Packet Loss",
            f"{metrics['packet_loss']}%"
        )

    with col3:
        st.metric(
            "CPU Usage",
            f"{metrics['cpu_usage']}%"
        )


    st.write(
        f"**Location:** {analysis['location']}"
    )


    # --------------------------------
    # Severity information
    # --------------------------------

    st.subheader(
        "🚨 Automated Analysis"
    )

    st.json(
        analysis["analysis"]
    )


    st.divider()


    # --------------------------------
    # AI Agent
    # --------------------------------

    st.subheader(
        "🤖 Ask the AI Network Agent"
    )

    default_question = (
        f"Analyze network node {selected_node} "
        "and explain if there is a problem."
    )

    question = st.text_area(
        "Question",
        value=default_question
    )

    if st.button(
        "Run AI Analysis",
        type="primary"
    ):

        with st.spinner(
            "Agent is analyzing the network..."
        ):

            try:

                answer = ask_agent(
                    question
                )

                st.success(
                    "Analysis complete"
                )

                st.markdown(
                    answer
                )

            except Exception as error:

                st.error(
                    f"Agent error: {error}"
                )


except requests.RequestException:

    st.error(
        """
        Network API is not running.

        Start it in another terminal with:

        uvicorn network_api:app --reload
        """
    )