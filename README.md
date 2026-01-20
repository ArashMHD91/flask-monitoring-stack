# Flask Monitoring Stack - Complete Beginner's Guide

A hands-on tutorial for building a production-grade monitoring system from scratch. Perfect for learning SRE (Site Reliability Engineering), Docker, Prometheus, and Grafana.

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat&logo=Prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=flat&logo=grafana&logoColor=white)
![Time](https://img.shields.io/badge/time-2--3%20hours-blue.svg)

---

## 📋 What You'll Build

By the end of this guide, you'll have:

- ✅ A Flask web application exposing metrics
- ✅ A complete monitoring stack running in Docker
- ✅ Real-time dashboards showing CPU, memory, and service status
- ✅ Automated alerts that fire when things go wrong
- ✅ A portfolio-ready project with validation through failure testing

**Perfect for beginners!** No prior experience required.

---

## 📦 What You Need

### Required Software

1. **Docker Desktop**

2. **Text Editor**

### Verify Installation

Open terminal/command prompt and run:

```bash
docker --version
docker-compose --version
```

You should see version numbers. If yes, you're ready! 🎉

---

# 🚀 Step-by-Step Tutorial

---

## STEP 1: Create Project Folders

Open your terminal and run:

```bash
# Create main folder
mkdir flask-monitoring-stack
cd flask-monitoring-stack

# Create subfolders
mkdir app
mkdir prometheus
```

**Your structure:**
```
flask-monitoring-stack/
├── app/
└── prometheus/
```

---

## STEP 2: Create Flask Application

Navigate to app folder:

```bash
cd app
```

Create `app.py` file (use any text editor):

```python
from flask import Flask, jsonify
import psutil
import time

app = Flask(__name__)

# Homepage
@app.route('/')
def home():
    return "Hello! I'm a monitored Flask application! 👋"

# Health check endpoint
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time()
    }), 200

# Metrics endpoint for Prometheus
@app.route('/metrics')
def metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    metrics_output = f"""# HELP cpu_usage_percent Current CPU usage
# TYPE cpu_usage_percent gauge
cpu_usage_percent {cpu_percent}

# HELP memory_usage_percent Current memory usage
# TYPE memory_usage_percent gauge
memory_usage_percent {memory.percent}

# HELP app_up Application is running
# TYPE app_up gauge
app_up 1
"""
    return metrics_output, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

**Save this file as `app.py`**

---

## STEP 3: Create Dockerfile

In the same `app` folder, create `Dockerfile` (no extension):

```dockerfile
# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install flask psutil

# Copy application
COPY app.py .

# Expose port
EXPOSE 8080

# Run application
CMD ["python", "app.py"]
```

**Save as `Dockerfile`** (exactly this name, no .txt extension)

---

## STEP 4: Create Prometheus Configuration

Go back and enter prometheus folder:

```bash
cd ..
cd prometheus
```

Create `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - '/etc/prometheus/alert_rules.yml'

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'flask-app'
    static_configs:
      - targets: ['app:8080']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

**Save as `prometheus.yml`**

---

## STEP 5: Create Alert Rules

Still in `prometheus` folder, create `alert_rules.yml`:

```yaml
groups:
  - name: service_alerts
    interval: 10s
    rules:
      - alert: ServiceDown
        expr: up{job="flask-app"} == 0
        for: 30s
        labels:
          severity: critical
        annotations:
          summary: "Flask application is down"
          description: "The Flask app has been unreachable for more than 30 seconds"

      - alert: HighCPUUsage
        expr: cpu_usage_percent > 80
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage is above 80% for more than 1 minute"

      - alert: HighMemoryUsage
        expr: memory_usage_percent > 85
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "Memory usage is above 85%"
```

**Save as `alert_rules.yml`**

---

## STEP 6: Create Docker Compose File

Go back to main folder:

```bash
cd ..
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: ./app
    container_name: flask-app
    ports:
      - "8080:8080"
    networks:
      - monitoring
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus/alert_rules.yml:/etc/prometheus/alert_rules.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    networks:
      - monitoring
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana
    networks:
      - monitoring
    restart: unless-stopped

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - "9100:9100"
    networks:
      - monitoring
    restart: unless-stopped

networks:
  monitoring:
    driver: bridge

volumes:
  grafana-storage:
```

**Save as `docker-compose.yml`**

---

## STEP 7: Verify File Structure

Check your files:

```bash
ls -R
```

**Should show:**
```
flask-monitoring-stack/
├── app/
│   ├── Dockerfile
│   └── app.py
├── prometheus/
│   ├── prometheus.yml
│   └── alert_rules.yml
└── docker-compose.yml
```

✅ If this matches, continue!

---

## STEP 8: Start Everything

From the main folder, run:

```bash
docker-compose up -d
```

**This will:**
- Download images (first time takes 2-5 minutes)
- Build Flask app
- Start all 4 containers

**Wait for it to complete. You'll see:**
```
Creating network "flask-monitoring-stack_monitoring" ... done
Creating flask-app ... done
Creating prometheus ... done
Creating grafana ... done
Creating node-exporter ... done
```

---

## STEP 9: Verify Containers Running

```bash
docker-compose ps
```

**All 4 should show "Up":**
```
NAME            STATUS
flask-app       Up
prometheus      Up
grafana         Up
node-exporter   Up
```

✅ Perfect! Everything is running.

---

## STEP 10: Test Flask Application

Open browser, visit these URLs:

**1. Homepage:** http://localhost:8080
- Should show: "Hello! I'm a monitored Flask application! 👋"

**2. Health:** http://localhost:8080/health
- Should show JSON with "healthy" status

**3. Metrics:** http://localhost:8080/metrics
- Should show metrics like `cpu_usage_percent`, `memory_usage_percent`, `app_up 1`

✅ If all three work, Flask is perfect!

---

## STEP 11: Verify Prometheus

Open: http://localhost:9090

**Check Targets:**
1. Click "Status" → "Targets"
2. Should see 3 targets, all **UP (green)**:
   - prometheus
   - flask-app
   - node-exporter

**Test a Query:**
1. Click "Graph" tab
2. Type: `up{job="flask-app"}`
3. Click "Execute"
4. Should show value **1**

**Check Alerts:**
1. Click "Alerts" tab
2. Should see 3 alerts (all green/inactive):
   - ServiceDown
   - HighCPUUsage
   - HighMemoryUsage

✅ Prometheus is working!

---

## STEP 12: Configure Grafana - Add Data Source

Open: http://localhost:3000

**Login:**
- Username: `admin`
- Password: `admin`
- (Skip password change if prompted)

**Add Prometheus:**
1. Click ☰ menu (top left)
2. Go to: **Connections → Data sources**
3. Click **Add data source**
4. Select **Prometheus**
5. Set URL to: `http://prometheus:9090` ⚠️ **Exactly this!**
6. Scroll down, click **Save & Test**
7. Should see green ✅ "Successfully queried"

✅ Data source connected!

---

## STEP 13: Import Node Exporter Dashboard

1. Click ☰ → **Dashboards**
2. Click **New** → **Import**
3. Enter ID: `1860`
4. Click **Load**
5. Select **Prometheus** as data source
6. Click **Import**

🎉 **You now have a beautiful system dashboard!**

Explore it - see CPU, memory, disk, network graphs with live data.

---

## STEP 14: Create Custom Dashboard - Panel 1 (App Status)

1. Click ☰ → **Dashboards**
2. Click **New** → **New Dashboard**
3. Click **Add visualization**
4. Select **Prometheus**

**Configure Query:**
1. Click **Code** button (top right of query area)
2. Type: `up{job="flask-app"}`
3. Click **Run queries**

**Configure Panel:**
1. Change **Visualization** (top right) from "Time series" to **Stat**
2. In right sidebar, **Title**: type `App Status`
3. Scroll to **Standard options → Thresholds**:
   - Base: **Red** (for value 0)
   - Click **+ Add threshold**
   - Value: `1`, Color: **Green**
4. Click **Apply** (top right)

✅ Should show green **1**!

---

## STEP 15: Create Panel 2 (CPU Usage)

1. Click **Add** → **Visualization**
2. Select **Prometheus**
3. Query (Code mode): `cpu_usage_percent`
4. Click **Run queries**
5. Title: `CPU Usage %`
6. Keep visualization as **Time series**
7. Click **Apply**

✅ Should show CPU graph!

---

## STEP 16: Create Panel 3 (Memory Usage)

1. Click **Add** → **Visualization**
2. Select **Prometheus**
3. Query: `memory_usage_percent`
4. Click **Run queries**
5. Title: `Memory Usage %`
6. Visualization: **Time series** or **Gauge**
7. Click **Apply**

✅ Three panels complete!

---

## STEP 17: Save Dashboard

1. Click 💾 **Save** icon (top right)
2. Name: `Flask App Monitoring`
3. Click **Save**

🎉 **Your custom dashboard is ready!**

---

## STEP 18: Test Failure - Service Down

**Stop Flask app:**

```bash
docker stop flask-app
```

**Wait 60 seconds**, then check:

**Prometheus Targets:** http://localhost:9090/targets
- flask-app should be **RED (DOWN)** 🔴

**Prometheus Alerts:** http://localhost:9090/alerts
- ServiceDown should go **ORANGE** (pending) → **RED** (firing) 🚨

**Grafana Dashboard:** http://localhost:3000
- App Status should show **0 (RED)** 🔴

📸 **Take screenshots!**

**Restart app:**

```bash
docker start flask-app
```

Wait 30 seconds - everything should return to green! ✅

---

## STEP 19: Test Failure - High CPU

**Generate CPU load:**

```bash
# Enter container
docker exec -it flask-app bash

# Install stress tool
apt-get update
apt-get install -y stress

# Generate load for 2 minutes
stress --cpu 2 --timeout 120s

# Exit
exit
```

**Watch in Grafana:**
- CPU Usage % graph should spike! 📈

**After 1 minute, check Prometheus Alerts:**
- HighCPUUsage should fire (RED) 🔴

📸 **Screenshot the spike!**

---

## STEP 20: Completion Checklist

Check everything works:

- [ ] All 4 containers running
- [ ] Flask app accessible at http://localhost:8080
- [ ] Prometheus targets all UP
- [ ] Grafana dashboards showing data
- [ ] ServiceDown alert tested (fired when app stopped)
- [ ] CPU alert tested (fired during load)

✅ **If all checked, you're done!** 🎉

---

## 📊 What You Built

```
┌─────────────────────────────────────────┐
│         Docker Network                  │
│                                         │
│  ┌──────────┐      ┌──────────┐         │
│  │Flask App │◄─────┤Prometheus│         │
│  │Port: 8080│      │Port: 9090│         │
│  └──────────┘      └────┬─────┘         │
│                         │               │
│  ┌──────────┐           │  ┌─────────┐  │
│  │   Node   │◄──────────┴─►│ Grafana │  │
│  │ Exporter │              │Port: 3000  │
│  └──────────┘              └─────────┘  │
└─────────────────────────────────────────┘
```

**Components:**
- **Flask App**: Your application being monitored
- **Prometheus**: Collects and stores metrics every 15s
- **Grafana**: Visualizes metrics in dashboards
- **Node Exporter**: Provides system-level metrics

---

## 🎓 Questions & Answers

### Q: Why use Docker?

**A:** Docker ensures the application runs consistently everywhere—my laptop, a colleague's machine, or production. It packages the app with all dependencies into a container, eliminating "works on my machine" problems. For this project, Docker Compose orchestrates 4 services with one command, making the entire stack reproducible.

---

### Q: What is Prometheus and how does it work?

**A:** Prometheus is a time-series database for monitoring. It uses a "pull model"—actively scraping HTTP endpoints every 15 seconds instead of applications pushing data. It stores metrics with timestamps and labels, allowing historical queries like "what was CPU usage 2 hours ago?" Prometheus also continuously evaluates alert rules and fires alerts when conditions are met.

---

### Q: Why use `up{job="flask-app"}` instead of `app_up`?

**A:** `app_up` is a custom metric we defined—it's reported by the Flask app and equals 1 when running. But when the container stops, this metric disappears (no one to report it).

`up{job="flask-app"}` is automatically generated by Prometheus for every target. It's 1 when Prometheus successfully scrapes and 0 when it fails. This metric exists even when the container is stopped, making it reliable for alerting. That's why our ServiceDown alert uses `up{job="flask-app"} == 0`.

---

### Q: How do containers communicate?

**A:** Docker Compose creates a bridge network where containers communicate using service names as hostnames. When Grafana connects to `http://prometheus:9090`, Docker's DNS resolves "prometheus" to the Prometheus container's IP. This is why we use container names, not `localhost`—each container has its own localhost.

---

### Q: Why do alerts have a `for:` duration?

**A:** The `for: 30s` prevents false alarms. Without it, a brief network hiccup would trigger an alert immediately. By waiting 30 seconds, we confirm the issue is sustained and actionable. This prevents alert fatigue—too many false alerts cause engineers to ignore them, defeating the purpose.

---

### Q: Why simulate failures?

**A:** Failure simulation validates that monitoring actually works. It's not enough to build dashboards—you need proof they'll catch real issues. By stopping the Flask app, we confirmed:
1. Prometheus detected the outage
2. The alert fired as configured
3. Grafana showed correct status

This is chaos engineering—intentionally breaking things builds confidence in your monitoring.

---

### Q: How would you improve this for production?

**A:** For production, I'd add:
1. **AlertManager** for notifications (Slack, email, PagerDuty)
2. **Persistent storage** for Prometheus data
3. **HTTPS and authentication** for all endpoints
4. **High availability** with multiple Prometheus instances
5. **More metrics** (request latency, error rates, business metrics)
6. **Log aggregation** (ELK or Loki)
7. **Distributed tracing** (Jaeger)
8. **Service discovery** for dynamic environments
9. **Backup procedures**

---

## 🔧 Troubleshooting

### Problem: "No data" in Grafana

**Solutions:**
1. Check Prometheus targets: http://localhost:9090/targets (all should be UP)
2. Verify metrics: `curl http://localhost:8080/metrics`
3. Set Grafana time range to "Last 5 minutes"
4. Wait 30 seconds for data collection
5. Use `up{job="flask-app"}` instead of `app_up`

---

### Problem: Alerts not firing

**Solutions:**
1. Check config loaded: http://localhost:9090/config
2. Restart Prometheus: `docker restart prometheus`
3. Wait full duration (60-90 seconds total)
4. Verify YAML syntax (indentation matters!)

---

### Problem: Can't access services

**Solutions:**
1. Verify containers: `docker-compose ps` (all should be "Up")
2. Check ports aren't in use
3. Restart: `docker-compose down && docker-compose up -d`
4. Check logs: `docker logs flask-app`

---

### Problem: Grafana can't connect to Prometheus

**Solution:**
URL must be `http://prometheus:9090` (not `localhost:9090`)

Use container name, not localhost!

---

## 🛑 Stopping the Project

**Stop services:**
```bash
docker-compose down
```

**Stop and remove all data:**
```bash
docker-compose down -v
```

**Restart from scratch:**
```bash
docker-compose down -v
docker rmi flask-monitoring-stack-app
docker-compose up -d
```

**Learning resources:**
- [Google SRE Book](https://sre.google/books/) (free)
- [Prometheus Docs](https://prometheus.io/docs/)
- [Grafana Tutorials](https://grafana.com/tutorials/)

---

## 🙏 Credits

- Prometheus community
- Grafana Labs
- Docker
- The SRE community

---

## 📄 License

MIT License - feel free to use for learning!

---

**🎉 CONGRATULATIONS! You built a complete monitoring system!**

**Built with ❤️ for learning SRE**

---

**Questions? Issues? Open an issue on GitHub!**
**Found this helpful? Star it on GitHub! ⭐**
