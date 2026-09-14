from pydantic import BaseModel


class NetworkNode(BaseModel):
    node_id: str
    location: str
    latency_ms: float
    packet_loss: float
    cpu_usage: float
    status: str