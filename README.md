# 📊 Visualizing Data with Grafana

> 🚀 A comprehensive hands-on lab for building a complete observability and monitoring stack using **Grafana, Prometheus, Jaeger, Loki, OpenTelemetry, Docker, and Python**.

---

## 📌 Table of Contents

* 🎯 [Lab Objectives](#-lab-objectives)
* 🛠️ [Technologies Used](#️-technologies-used)
* 📋 [Prerequisites](#-prerequisites)
* 🏗️ [Architecture](#️-architecture)
* 🚀 [Lab Tasks](#-lab-tasks)
* 📊 [Dashboards](#-dashboards)
* 🔔 [Alerting](#-alerting)
* 🧪 [Testing and Validation](#-testing-and-validation)
* 🛠️ [Troubleshooting](#️-troubleshooting)
* 🎓 [Conclusion](#-conclusion)

---

## 🎯 Lab Objectives

By completing this lab, you will learn how to:

* ✅ Install and configure Grafana on Linux
* 📈 Configure Prometheus as a metrics data source
* 🔍 Configure Jaeger for distributed tracing
* 📊 Create comprehensive Grafana dashboards
* ⚡ Visualize OpenTelemetry metrics and traces
* 🔧 Build custom panels using PromQL queries
* 🔗 Integrate OpenTelemetry, Prometheus, Jaeger, and Grafana
* 🚨 Configure monitoring and alerting capabilities

---

## 🛠️ Technologies Used

<p align="center">

![Grafana](https://img.shields.io/badge/Grafana-Visualization-orange?style=for-the-badge\&logo=grafana)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-orange?style=for-the-badge\&logo=prometheus)
![Jaeger](https://img.shields.io/badge/Jaeger-Tracing-blue?style=for-the-badge)
![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-Observability-blue?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Containers-blue?style=for-the-badge\&logo=docker)
![Python](https://img.shields.io/badge/Python-Application-yellow?style=for-the-badge\&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_App-black?style=for-the-badge\&logo=flask)
![Loki](https://img.shields.io/badge/Loki-Logging-yellow?style=for-the-badge)

</p>

---

## 📋 Prerequisites

Before starting this lab, you should have:

* 🐧 Basic knowledge of Linux commands
* 🐳 Understanding of Docker and containers
* 📊 Basic knowledge of monitoring concepts
* 🔍 Understanding of metrics and distributed tracing
* 📝 Familiarity with YAML configuration files
* 🌐 Basic understanding of HTTP and web applications

---

# 🏗️ Architecture

The complete observability pipeline works as follows:

```text
                    ┌─────────────────────┐
                    │   Sample Flask App  │
                    │                     │
                    │ Metrics + Traces    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ OpenTelemetry       │
                    │ Collector           │
                    └───────┬───────┬─────┘
                            │       │
               Metrics      │       │ Traces
                            │       │
                            ▼       ▼
                     ┌──────────┐ ┌──────────┐
                     │Prometheus│ │  Jaeger  │
                     └─────┬────┘ └────┬─────┘
                           │           │
                           └─────┬─────┘
                                 ▼
                        ┌────────────────┐
                        │    Grafana     │
                        │ Dashboards &   │
                        │ Visualization  │
                        └────────────────┘
```

---

# 🚀 Lab Tasks

## 🐳 Task 1: Install Docker and Docker Compose

Install Docker and required dependencies:

```bash
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
```

Install Docker Engine:

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io
```

Start and enable Docker:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

Add your user to the Docker group:

```bash
sudo usermod -aG docker $USER
```

Apply the group changes:

```bash
newgrp docker
```

---

## 📁 Task 2: Create the Monitoring Environment

Create the project directory:

```bash
mkdir -p ~/grafana-lab
cd ~/grafana-lab
```

Create configuration directories:

```bash
mkdir -p config/prometheus
mkdir -p config/grafana
mkdir -p config/jaeger

mkdir -p data/prometheus
mkdir -p data/grafana
```

---

## 📈 Task 3: Configure Prometheus

Prometheus collects metrics from multiple services.

Configured targets include:

* 📊 Prometheus
* 🚀 Sample Application
* 🔭 OpenTelemetry Collector
* 🖥️ Node Exporter

Example metrics endpoint:

```text
sample-app:8080/metrics
```

Prometheus also collects OpenTelemetry metrics and system metrics.

---

## 🔭 Task 4: Configure OpenTelemetry Collector

The OpenTelemetry Collector receives telemetry data from applications.

### Supported protocols

* ⚡ OTLP gRPC — Port `4317`
* 🌐 OTLP HTTP — Port `4318`

### Data pipelines

```text
Application
     │
     ▼
OpenTelemetry Collector
     │
 ┌───┴────┐
 ▼        ▼
Metrics   Traces
 ▼        ▼
Prometheus Jaeger
```

The collector processes telemetry using:

* 📦 Batch Processor
* 🧠 Memory Limiter
* 📊 Prometheus Exporter
* 🔍 Jaeger Exporter

---

## 🖥️ Task 5: Configure Grafana Data Sources

Grafana is configured with the following data sources:

### 📊 Prometheus

Used for:

* Application metrics
* Infrastructure monitoring
* Performance statistics

### 🔍 Jaeger

Used for:

* Distributed tracing
* Request analysis
* Performance troubleshooting

### 📜 Loki

Used for:

* Centralized log visualization
* Log analysis
* Application troubleshooting

---

# 🐍 Task 6: Create the Sample Application

A Python Flask application is created to generate:

* 📈 Metrics
* 🔍 Distributed traces
* 🌐 HTTP requests
* ⏱️ Request duration data

### Application Endpoints

| Endpoint     | Description                |
| ------------ | -------------------------- |
| `/`          | Main application endpoint  |
| `/api/users` | Returns sample users       |
| `/api/slow`  | Simulates a slow request   |
| `/metrics`   | Exposes Prometheus metrics |
| `/health`    | Application health check   |

---

## 📊 Application Metrics

The application generates metrics such as:

```text
http_requests_total
http_request_duration_seconds
active_connections
flask_requests_total
flask_request_duration_seconds
flask_active_users
```

These metrics help monitor:

* 🚀 Request rates
* ⏱️ Response times
* 👥 Active users
* ⚠️ Application performance

---

# 🐳 Task 7: Build the Monitoring Stack

The Docker Compose environment contains the following services:

| Service                    | Purpose              | Port           |
| -------------------------- | -------------------- | -------------- |
| 🟠 Grafana                 | Visualization        | `3000`         |
| 🔥 Prometheus              | Metrics monitoring   | `9090`         |
| 🔍 Jaeger                  | Distributed tracing  | `16686`        |
| 📡 OpenTelemetry Collector | Telemetry processing | `4317`, `4318` |
| 🖥️ Node Exporter          | System metrics       | `9100`         |
| 📜 Loki                    | Log aggregation      | `3100`         |
| 🚀 Sample App              | Demo application     | `8080`         |

---

## ▶️ Start the Stack

Set permissions:

```bash
sudo chown -R 472:472 data/grafana
sudo chown -R 65534:65534 data/prometheus
```

Start all containers:

```bash
docker-compose up -d
```

Check service status:

```bash
docker-compose ps
```

View logs:

```bash
docker-compose logs -f --tail=50
```

---

# 🚦 Task 8: Generate Application Traffic

The lab includes a Python traffic generator.

It sends requests to:

```text
/
 /api/users
 /api/slow
 /health
```

Install Python requests:

```bash
pip3 install requests
```

Run the traffic generator:

```bash
python3 generate_traffic.py &
```

This generates realistic traffic for monitoring dashboards and traces.

---

# 🌐 Task 9: Access the Monitoring Services

### 🟠 Grafana

```text
http://localhost:3000
```

### 🔥 Prometheus

```text
http://localhost:9090
```

### 🔍 Jaeger

```text
http://localhost:16686
```

### 🚀 Sample Application

```text
http://localhost:8080
```

---

# 📊 Dashboards

## 🚀 Application Performance Dashboard

Create panels for:

### 📈 HTTP Request Rate

```promql
rate(flask_requests_total[5m])
```

### ⏱️ Request Duration

```promql
histogram_quantile(
  0.95,
  rate(flask_request_duration_seconds_bucket[5m])
)
```

### 👥 Active Users

```promql
flask_active_users
```

### ⚠️ Error Rate

```promql
rate(flask_requests_total{code!="200"}[5m])
/
rate(flask_requests_total[5m])
* 100
```

---

## 🖥️ System Metrics Dashboard

### CPU Usage

```promql
100 - (
  avg by (instance)
  (
    irate(node_cpu_seconds_total{mode="idle"}[5m])
  ) * 100
)
```

### Memory Usage

```promql
(
  1 -
  (
    node_memory_MemAvailable_bytes
    /
    node_memory_MemTotal_bytes
  )
) * 100
```

### Disk Usage

```promql
100 - (
  (
    node_filesystem_avail_bytes{mountpoint="/"}
    /
    node_filesystem_size_bytes{mountpoint="/"}
  ) * 100
)
```

### Network Traffic

```promql
rate(node_network_receive_bytes_total[5m])
```

```promql
rate(node_network_transmit_bytes_total[5m])
```

---

# 🔍 Trace Visualization

Grafana can visualize distributed traces through Jaeger.

Steps:

1. 🔎 Open **Grafana Explore**
2. 📡 Select **Jaeger** as the data source
3. 🚀 Select the `sample-app` service
4. ▶️ Run the query
5. 🔍 Analyze traces and request operations

This helps identify:

* Slow requests
* Database operations
* Service dependencies
* Performance bottlenecks

---

# 🔔 Alerting

## ⚠️ High Response Time Alert

Monitor slow requests using:

```promql
histogram_quantile(
  0.95,
  rate(flask_request_duration_seconds_bucket[5m])
)
```

Example condition:

```text
IS ABOVE 2 seconds
```

---

## 🚨 High Error Rate Alert

Monitor application errors using:

```promql
rate(flask_requests_total{code!="200"}[5m])
/
rate(flask_requests_total[5m])
* 100
```

Example condition:

```text
IS ABOVE 5%
```

---

# 🔥 Advanced Visualizations

## 🕸️ Service Map

Use the **Node Graph** visualization to display service relationships.

Example:

```text
Service A
    │
    ▼
Service B
    │
    ▼
Database
```

---

## 🌡️ Request Duration Heatmap

Use a heatmap to visualize request latency:

```promql
sum(
  rate(flask_request_duration_seconds_bucket[5m])
) by (le)
```

This helps identify latency distribution and slow requests.

---

# 💾 Dashboard Backup

Grafana dashboards can be exported and imported as JSON files.

You can:

1. 📤 Export dashboards
2. 💾 Save dashboard JSON
3. 📥 Import dashboards
4. 🔄 Restore dashboards on another Grafana instance

This makes dashboard management easier and supports infrastructure automation.

---

# 🧪 Testing and Validation

## 🚀 Generate Normal Traffic

```bash
for i in {1..10}; do
  curl http://localhost:8080/
  sleep 1
done
```

---

## 🐢 Generate Slow Requests

```bash
for i in {1..5}; do
  curl http://localhost:8080/api/slow
  sleep 2
done
```

---

## 👥 Generate API Requests

```bash
for i in {1..15}; do
  curl http://localhost:8080/api/users
  sleep 0.5
done
```

---

## 📊 Verify Metrics

Check Prometheus metrics:

```bash
curl "http://localhost:9090/api/v1/query?query=up"
```

Check application metrics:

```bash
curl http://localhost:8080/metrics
```

Check OpenTelemetry metrics:

```bash
curl http://localhost:8889/metrics
```

---

# 🛠️ Troubleshooting

## 🔍 Check Service Health

```bash
curl -f http://localhost:3000/api/health
```

```bash
curl -f http://localhost:9090/-/healthy
```

```bash
curl -f http://localhost:16686/
```

```bash
curl -f http://localhost:8080/health
```

---

## 📡 Check Prometheus Targets

```bash
curl http://localhost:9090/api/v1/targets
```

---

## 📜 Check Container Logs

```bash
docker-compose logs --tail=100
```

Check specific services:

```bash
docker-compose logs grafana
docker-compose logs prometheus
docker-compose logs jaeger
docker-compose logs sample-app
```

---

# 🎯 Key Learning Outcomes

After completing this lab, you will understand how to:

* 🟠 Build Grafana dashboards
* 🔥 Monitor infrastructure with Prometheus
* 🔍 Analyze distributed traces with Jaeger
* 📡 Process telemetry using OpenTelemetry
* 🐳 Deploy a complete monitoring stack using Docker Compose
* 📊 Create custom PromQL queries
* 🚨 Configure performance alerts
* 🌡️ Build advanced visualizations
* 🛠️ Troubleshoot observability services

---

# 🏆 Complete Observability Pipeline

```text
┌───────────────┐
│  Application  │
│ Flask + OTel  │
└───────┬───────┘
        │
        ▼
┌───────────────────┐
│ OpenTelemetry     │
│ Collector         │
└───────┬───────────┘
        │
   ┌────┴────┐
   ▼         ▼
Metrics     Traces
   │         │
   ▼         ▼
Prometheus  Jaeger
   │         │
   └────┬────┘
        ▼
   ┌─────────┐
   │ Grafana │
   └─────────┘
        │
        ▼
 Dashboards & Alerts
```

---

# 🎓 Conclusion

🎉 In this lab, you successfully built a complete observability environment.

You learned how to:

* 📊 Visualize application and infrastructure metrics
* 🔍 Analyze distributed traces
* 📡 Collect telemetry with OpenTelemetry
* 🔥 Monitor services using Prometheus
* 🟠 Build powerful Grafana dashboards
* 📜 Integrate logging with Loki
* 🚨 Configure monitoring alerts
* 🛠️ Troubleshoot monitoring services

The completed architecture provides a strong foundation for modern **DevOps**, **Cloud Monitoring**, **Site Reliability Engineering (SRE)**, and **Observability** practices.

---

## 👨‍💻 Author

**Hafiz Muhammad Salman**

### ☁️ Cloud DevOps Engineer | Linux Administrator

<p align="center">

⭐ If you found this lab useful, consider giving the repository a star!

**Happy Monitoring! 🚀📊🔍**

</p>
