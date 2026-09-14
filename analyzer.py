import numpy as np


def analyze_metrics(
    latency_ms,
    packet_loss,
    cpu_usage
):

    # Convert incoming values to normal floats
    latency_ms = float(latency_ms)
    packet_loss = float(packet_loss)
    cpu_usage = float(cpu_usage)

    # ----------------------------
    # Latency score
    # ----------------------------

    latency_score = np.select(
        [
            latency_ms >= 150,
            latency_ms >= 80
        ],
        [
            2,
            1
        ],
        default=0
    )

    # ----------------------------
    # Packet loss score
    # ----------------------------

    packet_loss_score = np.select(
        [
            packet_loss >= 10,
            packet_loss >= 3
        ],
        [
            2,
            1
        ],
        default=0
    )

    # ----------------------------
    # CPU score
    # ----------------------------

    cpu_score = np.select(
        [
            cpu_usage >= 90,
            cpu_usage >= 75
        ],
        [
            2,
            1
        ],
        default=0
    )

    # Convert NumPy numbers to Python integers
    latency_score = int(latency_score)
    packet_loss_score = int(packet_loss_score)
    cpu_score = int(cpu_score)

    total_score = (
        latency_score
        + packet_loss_score
        + cpu_score
    )

    # ----------------------------
    # Severity
    # ----------------------------

    if total_score >= 5:
        severity = "critical"

    elif total_score >= 2:
        severity = "warning"

    else:
        severity = "healthy"

    return {
        "latency_score": latency_score,
        "packet_loss_score": packet_loss_score,
        "cpu_score": cpu_score,
        "total_score": int(total_score),
        "severity": severity
    }