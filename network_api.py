from fastapi import FastAPI, HTTPException
import pandas as pd

from models import NetworkNode
from analyzer import analyze_metrics


app = FastAPI(
    title="Network Monitoring API",
    description="Simulated REST API for telecom network monitoring",
    version="1.0.0"
)


DATA_PATH = "data/network_metrics.csv"


# --------------------------------
# Load network data
# --------------------------------

def load_network_data():

    df = pd.read_csv(
        DATA_PATH
    )

    return df


# --------------------------------
# Home endpoint
# --------------------------------

@app.get("/")
def home():

    return {
        "message": "Network API is running"
    }


# --------------------------------
# Get all network nodes
# --------------------------------

@app.get("/network/nodes")
def get_nodes():

    df = load_network_data()

    return df.to_dict(
        orient="records"
    )


# --------------------------------
# Get one network node
# --------------------------------

@app.get(
    "/network/status/{node_id}",
    response_model=NetworkNode
)
def get_network_status(
    node_id: str
):

    df = load_network_data()

    node = df[
        df["node_id"] == node_id
    ]

    if node.empty:

        raise HTTPException(
            status_code=404,
            detail="Network node not found"
        )

    node_data = node.iloc[0]

    return NetworkNode(
        node_id=node_data["node_id"],
        location=node_data["location"],
        latency_ms=node_data["latency_ms"],
        packet_loss=node_data["packet_loss"],
        cpu_usage=node_data["cpu_usage"],
        status=node_data["status"]
    )


# --------------------------------
# Analyze one network node
# --------------------------------

@app.get(
    "/network/analyze/{node_id}"
)
def analyze_network_node(
    node_id: str
):

    df = load_network_data()

    node = df[
        df["node_id"] == node_id
    ]

    if node.empty:

        raise HTTPException(
            status_code=404,
            detail="Network node not found"
        )

    node_data = node.iloc[0]

    analysis = analyze_metrics(
        latency_ms=node_data["latency_ms"],
        packet_loss=node_data["packet_loss"],
        cpu_usage=node_data["cpu_usage"]
    )

    return {
        "node_id": node_data["node_id"],
        "location": node_data["location"],

        "metrics": {
            "latency_ms": float(
                node_data["latency_ms"]
            ),

            "packet_loss": float(
                node_data["packet_loss"]
            ),

            "cpu_usage": float(
                node_data["cpu_usage"]
            )
        },

        "analysis": analysis
    }