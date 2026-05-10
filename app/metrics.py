from prometheus_client import Counter, Histogram, REGISTRY

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
    registry=REGISTRY,
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["endpoint"],
    registry=REGISTRY,
)

trainer_problems_generated = Counter(
    "trainer_problems_generated", "Total problems generated", registry=REGISTRY
)

trainer_answers_total = Counter(
    "trainer_answers_total", "Total answers submitted", ["result"], registry=REGISTRY
)
