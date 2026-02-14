# archivo: utils/metrics.py
from prometheus_client import Counter, Histogram

REQUEST_COUNTER = Counter(
    "openf1_proxy_requests_total",
    "Total proxy requests",
    ["endpoint"],
)

REQUEST_LATENCY = Histogram(
    "openf1_proxy_latency_seconds",
    "Latency of upstream requests",
    ["endpoint"],
)

CIRCUIT_BREAKER_STATE = Counter(
    "openf1_proxy_circuit_open_total",
    "Times circuit breaker opened",
)
