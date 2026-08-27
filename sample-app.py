import time
import random
import logging
from flask import Flask, request, jsonify
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create resource
resource = Resource.create({
    "service.name": "sample-app",
    "service.version": "1.0.0",
})

# Configure tracing
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Configure OTLP trace exporter
otlp_trace_exporter = OTLPSpanExporter(
    endpoint="http://otel-collector:4317",
    insecure=True
)

# Add span processor
span_processor = BatchSpanProcessor(otlp_trace_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Configure metrics
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(
        endpoint="http://otel-collector:4317",
        insecure=True
    ),
    export_interval_millis=5000
)

metrics.set_meter_provider(MeterProvider(
    resource=resource,
    metric_readers=[metric_reader]
))

meter = metrics.get_meter(__name__)

# Create metrics
request_counter = meter.create_counter(
    "http_requests_total",
    description="Total number of HTTP requests"
)

request_duration = meter.create_histogram(
    "http_request_duration_seconds",
    description="HTTP request duration in seconds"
)

active_connections = meter.create_up_down_counter(
    "active_connections",
    description="Number of active connections"
)

# Prometheus metrics
prom_request_counter = Counter('flask_requests_total', 'Total Flask requests', ['method', 'endpoint'])
prom_request_duration = Histogram('flask_request_duration_seconds', 'Flask request duration')
prom_active_users = Gauge('flask_active_users', 'Number of active users')

# Create Flask app
app = Flask(__name__)

# Instrument Flask
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.route('/metrics')
def metrics_endpoint():
    return generate_latest()

@app.route('/')
def home():
    with tracer.start_as_current_span("home_request") as span:
        start_time = time.time()
        
        # Add span attributes
        span.set_attribute("http.method", "GET")
        span.set_attribute("http.route", "/")
        
        # Simulate some work
        time.sleep(random.uniform(0.1, 0.5))
        
        # Update metrics
        request_counter.add(1, {"method": "GET", "endpoint": "/"})
        duration = time.time() - start_time
        request_duration.record(duration, {"method": "GET", "endpoint": "/"})
        
        # Update Prometheus metrics
        prom_request_counter.labels(method='GET', endpoint='/').inc()
        prom_request_duration.observe(duration)
        prom_active_users.set(random.randint(10, 100))
        
        return jsonify({
            "message": "Hello from Sample App!",
            "timestamp": time.time(),
            "duration": duration
        })

@app.route('/api/users')
def get_users():
    with tracer.start_as_current_span("get_users") as span:
        start_time = time.time()
        
        span.set_attribute("http.method", "GET")
        span.set_attribute("http.route", "/api/users")
        
        # Simulate database query
        with tracer.start_as_current_span("database_query") as db_span:
            db_span.set_attribute("db.operation", "SELECT")
            db_span.set_attribute("db.table", "users")
            time.sleep(random.uniform(0.05, 0.2))
        
        # Simulate some processing
        time.sleep(random.uniform(0.1, 0.3))
        
        duration = time.time() - start_time
        request_counter.add(1, {"method": "GET", "endpoint": "/api/users"})
        request_duration.record(duration, {"method": "GET", "endpoint": "/api/users"})
        
        prom_request_counter.labels(method='GET', endpoint='/api/users').inc()
        prom_request_duration.observe(duration)
        
        users = [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
        ]
        
        return jsonify(users)

@app.route('/api/slow')
def slow_endpoint():
    with tracer.start_as_current_span("slow_request") as span:
        start_time = time.time()
        
        span.set_attribute("http.method", "GET")
        span.set_attribute("http.route", "/api/slow")
        
        # Simulate slow operation
        sleep_time = random.uniform(1.0, 3.0)
        span.set_attribute("sleep.duration", sleep_time)
        time.sleep(sleep_time)
        
        duration = time.time() - start_time
        request_counter.add(1, {"method": "GET", "endpoint": "/api/slow"})
        request_duration.record(duration, {"method": "GET", "endpoint": "/api/slow"})
        
        prom_request_counter.labels(method='GET', endpoint='/api/slow').inc()
        prom_request_duration.observe(duration)
        
        return jsonify({
            "message": "This was a slow operation",
            "duration": duration
        })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": time.time()})

if __name__ == '__main__':
    logger.info("Starting sample application...")
    app.run(host='0.0.0.0', port=8080, debug=True)
