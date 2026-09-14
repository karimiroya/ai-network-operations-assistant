import requests

from langchain_core.tools import tool


API_BASE_URL = "http://127.0.0.1:8000"


@tool
def get_network_status(node_id: str) -> dict:
    """
    Get the current status and metrics of a telecom network node.

    Use this tool when the user asks about the current status,
    latency, packet loss, CPU usage, location, or metrics of a node.

    Example node_id: MI-204
    """

    url = f"{API_BASE_URL}/network/status/{node_id}"

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:

        return {
            "error": str(error)
        }


@tool
def analyze_network_node(node_id: str) -> dict:
    """
    Analyze a telecom network node and identify problems,
    severity, anomalies, or operational risk.

    Use this tool when the user asks whether a node has a
    problem or asks for analysis or diagnosis.

    Example node_id: MI-204
    """

    url = f"{API_BASE_URL}/network/analyze/{node_id}"

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:

        return {
            "error": str(error)
        }