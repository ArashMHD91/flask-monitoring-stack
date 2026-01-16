# Flask Monitoring Stack - Complete Step-by-Step Guide

A hands-on tutorial for building a production-grade monitoring system from scratch. Perfect for learning SRE (Site Reliability Engineering), Docker, Prometheus, and Grafana.

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat&logo=Prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=flat&logo=grafana&logoColor=white)
![Difficulty](https://img.shields.io/badge/difficulty-beginner-green.svg)
![Time](https://img.shields.io/badge/time-2--3%20hours-blue.svg)

---

## 📋 What You'll Build

By the end of this tutorial, you'll have:

- ✅ A Flask web application that exposes metrics
- ✅ A complete monitoring stack running in Docker containers
- ✅ Real-time dashboards in Grafana showing CPU, memory, and service status
- ✅ Automated alerts that fire when things go wrong
- ✅ A tested, validated monitoring system ready for your portfolio

**No prior experience required!** This guide assumes you're a complete beginner.

---

## 🎯 What You'll Learn

- **Docker**: How to containerize applications and orchestrate multiple services
- **Prometheus**: How to collect, store, and query metrics
- **Grafana**: How to build beautiful dashboards for data visualization
- **Alerting**: How to set up automated alerts for service failures
- **SRE Principles**: Core concepts of Site Reliability Engineering
- **Troubleshooting**: How to debug common monitoring issues

---

## ⏱️ Time Required

- **Setup & Installation**: 15-20 minutes
- **Building the Stack**: 45-60 minutes
- **Configuration & Testing**: 30-45 minutes
- **Total**: 2-3 hours (including breaks)

---

## 📦 Prerequisites

### Required Software

Before starting, install these tools:

1. **Docker Desktop** (includes Docker & Docker Compose)
2. **Text Editor**
3. **Terminal/Command Line Access**
   
### Verify Installation

Open your terminal and run:

```bash
docker --version
docker-compose --version
```

**Expected output:**
```
Docker version 20.10.x or higher
docker-compose version 1.29.x or higher
```

If you see version numbers, you're ready to start! 🎉

---

## 🏗️ Project Architecture

Here's what we're building:

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Network                          │
│                                                             │
│  ┌──────────────┐      ┌──────────────┐                     │
│  │  Flask App   │◄─────┤  Prometheus  │                     │
│  │  Port: 8080  │      │  Port: 9090  │                     │
│  │              │      │              │                     │
│  │ /metrics     │      │ - Collects   │                     │
│  │ /health      │      │ - Stores     │                     │
│  └──────────────┘      │ - Alerts     │                     │
│                        └──────┬───────┘                     │
│                               │                             │
│  ┌──────────────┐            │        ┌──────────────┐      │
│  │Node Exporter │◄───────────┘        │   Grafana    │      │
│  │ Port: 9100   │◄────────────────────┤  Port: 3000  │      │
│  │              │                     │              │      │
│  │ System       │                     │ Dashboards   │      │
│  │ Metrics      │                     │ Graphs       │      │
│  └──────────────┘                     └──────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
- **Flask App**: Your application (the thing being monitored)
- **Prometheus**: Collects and stores metrics
- **Grafana**: Visualizes metrics in dashboards
- **Node Exporter**: Provides system metrics (CPU, memory, disk)

---

# 🚀 Step-by-Step Tutorial

---

## PART 1: PROJECT SETUP

### Step 1: Create Project Folder Structure

Open your terminal and create the project folders:

```bash
# Create main project folder
mkdir flask-monitoring-stack
cd flask-monitoring-stack

# Create subfolders
mkdir app
mkdir prometheus
mkdir grafana
```

**What we just did:** Created an organized folder structure to keep our files neat.

**Folder structure so far:**
```
flask-monitoring-stack/
├── app/
├── prometheus/
└── grafana/
```

---

## PART 2: BUILD THE FLASK APPLICATION

### Step 2: Create the Flask Application

Navigate to the `app` folder and create the Python application:

```bash
cd app
```

Now create a file called `app.py`. You can use any text editor:

**Copy this code into `app.py`:**

```python
from flask import Flask, jsonify
import psutil
import time

app = Flask(__name__)

# Homepage - simple welcome message
@app.route('/')
def home():
    return "Hello! I'm a monitored Flask application! 👋"

# Health check endpoint - tells if the app is running
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time()
    }), 200

# Metrics endpoint - provides data for Prometheus
@app.route('/metrics')
def metrics():
    # Get current CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Get current memory usage
    memory = psutil.virtual_memory()
    
    # Format metrics in Prometheus format
    metrics_output = f"""# HELP cpu_usage_percent Current CPU usage percentage
# TYPE cpu_usage_percent gauge
cpu_usage_percent {cpu_percent}

# HELP memory_usage_percent Current memory usage percentage
# TYPE memory_usage_percent gauge
memory_usage_percent {memory.percent}

# HELP app_up Application is running
# TYPE app_up gauge
app_up 1
"""
    return metrics_output, 200, {'Content-Type': 'text/plain'}

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

**Save the file**

**What this code does:**
- **`/` endpoint**: A simple homepage that says hello
- **`/health` endpoint**: Returns JSON showing the app is healthy
- **`/metrics` endpoint**: Provides CPU and memory data in a format Prometheus understands

---

### Step 3: Create the Dockerfile

In the same `app` folder, create a file called `Dockerfile` (no file extension):

```bash
# If you're still in the app folder:
vim Dockerfile
```

**Copy this into the Dockerfile:**

```dockerfile
# Start with a Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install required Python packages
RUN pip install flask psutil

# Copy our application into the container
COPY app.py .

# Tell Docker this container uses port 8080
EXPOSE 8080

# Command to run when container starts
CMD ["python", "app.py"]
```

**Save the file.**

**What is a Dockerfile?**
Think of it as a recipe that tells Docker how to build a container for your app. Each line is a step in the recipe.

**What each line does:**
- `FROM python:3.9-slim` - Start with a minimal Python environment
- `WORKDIR /app` - Create a folder called /app inside the container
- `RUN pip install` - Install the Flask and psutil libraries
- `COPY app.py .` - Copy our Python file into the container
- `EXPOSE 8080` - Tell Docker our app listens on port 8080
- `CMD` - Run the app when the container starts

---

## PART 3: CONFIGURE PROMETHEUS

### Step 4: Create Prometheus Configuration

Go back to the main project folder and enter the prometheus folder:

```bash
cd ..
cd prometheus
```

Create a file called `prometheus.yml`:

```bash
vim prometheus.yml
```

**Copy this configuration:**

```yaml
# Global settings for Prometheus
global:
  scrape_interval: 15s       # How often to collect metrics
  evaluation_interval: 15s   # How often to evaluate alert rules

# Load alert rules from this file
rule_files:
  - '/etc/prometheus/alert_rules.yml'

# Configure what to monitor
scrape_configs:
  # Monitor Prometheus itself
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Monitor our Flask application
  - job_name: 'flask-app'
    static_configs:
      - targets: ['app:8080']

  # Monitor system metrics
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

**Save the file.**

**What this configuration does:**
- `scrape_interval: 15s` - Prometheus will check for new metrics every 15 seconds
- Each `job_name` defines something to monitor
- `targets` are the addresses where metrics are available
- Notice we use container names (like `app:8080`) instead of `localhost` - Docker networking!

---

### Step 5: Create Alert Rules

Still in the `prometheus` folder, create `alert_rules.yml`:

```bash
vim alert_rules.yml
```

**Copy these alert rules:**

```yaml
groups:
  - name: service_alerts
    interval: 10s
    rules:
      # Alert when the Flask app goes down
      - alert: ServiceDown
        expr: up{job="flask-app"} == 0
        for: 30s
        labels:
          severity: critical
        annotations:
          summary: "Flask application is down"
          description: "The Flask app has been unreachable for more than 30 seconds"

      # Alert when CPU usage is too high
      - alert: HighCPUUsage
        expr: cpu_usage_percent > 80
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage is above 80% for more than 1 minute"

      # Alert when memory usage is too high
      - alert: HighMemoryUsage
        expr: memory_usage_percent > 85
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "Memory usage is above 85% for more than 1 minute"
```

**Save the file.**

**Understanding alerts:**
- `expr: up{job="flask-app"} == 0` - The condition to check (is the app down?)
- `for: 30s` - Wait 30 seconds before firing (avoids false alarms)
- `severity: critical` - How serious is this problem?
- `annotations` - Human-readable descriptions of the alert

**Important note about the metric:**
We use `up{job="flask-app"}` instead of `app_up` because:
- `up` is automatically created by Prometheus for every target
- It exists even when the container is stopped
- `app_up` would disappear when the app stops (no one to report it!)

---

## PART 4: DOCKER COMPOSE ORCHESTRATION

### Step 6: Create Docker Compose File

Go back to the main project folder:

```bash
cd ..
```

Create `docker-compose.yml`:

```bash
vim docker-compose.yml
```

**Copy this configuration:**

```yaml
version: '3.8'

services:
  # Our Flask application
  app:
    build: ./app                    # Build from the Dockerfile in ./app
    container_name: flask-app
    ports:
      - "8080:8080"                 # Map port 8080 to your computer
    networks:
      - monitoring
    restart: unless-stopped

  # Prometheus - metrics collector
  prometheus:
    image: prom/prometheus:latest   # Use official Prometheus image
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      # Share config files with the container
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus/alert_rules.yml:/etc/prometheus/alert_rules.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    networks:
      - monitoring
    restart: unless-stopped

  # Grafana - visualization dashboard
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin       # Default username
      - GF_SECURITY_ADMIN_PASSWORD=admin   # Default password
    volumes:
      - grafana-storage:/var/lib/grafana   # Persist dashboard data
    networks:
      - monitoring
    restart: unless-stopped

  # Node Exporter - system metrics
  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - "9100:9100"
    networks:
      - monitoring
    restart: unless-stopped

# Create a network so containers can talk to each other
networks:
  monitoring:
    driver: bridge

# Create a volume to store Grafana data
volumes:
  grafana-storage:
```

**Save the file.**

**What is Docker Compose?**
Instead of starting each container manually with separate commands, Docker Compose lets us define all containers in one file and start them all with a single command!

**What each section does:**
- `services:` - Defines all the containers we want to run
- `build: ./app` - Build the Flask app from our Dockerfile
- `image: prom/prometheus:latest` - Download and use the official Prometheus image
- `ports: "8080:8080"` - Maps container port 8080 to your computer's port 8080
- `volumes:` - Shares files between your computer and the container
- `networks:` - Puts all containers on the same network so they can communicate
- `restart: unless-stopped` - Automatically restart if the container crashes

---

## PART 5: START THE MONITORING STACK

### Step 7: Launch All Services

You should now be in the main project folder (`flask-monitoring-stack`). Let's verify your file structure:

```bash
ls -R
```

**You should see:**
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

**If everything looks good, start the stack:**

```bash
docker-compose up -d
```

**What happens next:**
1. Docker downloads the required images (Prometheus, Grafana, Node Exporter)
2. Docker builds your Flask application
3. All four containers start
4. The `-d` flag means "detached" (runs in the background)

**This might take 2-5 minutes the first time!**

**You'll see output like:**
```
Creating network "flask-monitoring-stack_monitoring" ... done
Creating volume "flask-monitoring-stack_grafana-storage" ... done
Building app...
...
Creating flask-app ... done
Creating prometheus ... done
Creating grafana ... done
Creating node-exporter ... done
```

---

### Step 8: Verify Everything is Running

Check that all containers are up:

```bash
docker-compose ps
```

**Expected output:**
```
NAME            IMAGE                      STATUS
flask-app       flask-monitoring-app       Up
prometheus      prom/prometheus:latest     Up
grafana         grafana/grafana:latest     Up
node-exporter   prom/node-exporter:latest  Up
```

**All four containers should show "Up"!**

**If a container is not up:**
```bash
# Check the logs for that container
docker logs flask-app
docker logs prometheus
docker logs grafana
docker logs node-exporter
```

---

## PART 6: VERIFY THE FLASK APPLICATION

### Step 9: Test the Flask Endpoints

Open your web browser and visit these URLs:

**1. Homepage:**
```
http://localhost:8080
```
**Expected:** Should show: "Hello! I'm a monitored Flask application! 👋"

**2. Health Check:**
```
http://localhost:8080/health
```
**Expected:** Should show JSON:
```json
{
  "status": "healthy",
  "timestamp": 1234567890.123
}
```

**3. Metrics Endpoint:**
```
http://localhost:8080/metrics
```
**Expected:** Should show:
```
# HELP cpu_usage_percent Current CPU usage percentage
# TYPE cpu_usage_percent gauge
cpu_usage_percent 5.2

# HELP memory_usage_percent Current memory usage percentage
# TYPE memory_usage_percent gauge
memory_usage_percent 45.3

# HELP app_up Application is running
# TYPE app_up gauge
app_up 1
```

✅ **If all three endpoints work, your Flask app is running correctly!**

---

## PART 7: CONFIGURE PROMETHEUS

### Step 10: Access Prometheus

Open your browser and go to:
```
http://localhost:9090
```

**You should see the Prometheus web interface!**

---

### Step 11: Verify Targets are Being Monitored

1. **Click on "Status"** in the top menu
2. **Select "Targets"** from the dropdown

**You should see 3 targets:**

| Endpoint | State | Labels |
|----------|-------|--------|
| prometheus (localhost:9090) | UP 🟢 | job="prometheus" |
| flask-app (app:8080) | UP 🟢 | job="flask-app" |
| node-exporter (node-exporter:9100) | UP 🟢 | job="node-exporter" |

**All three should show "State: UP" in green!**

**If any target is DOWN (red):**
- Wait 15-30 seconds and refresh (Prometheus scrapes every 15 seconds)
- Check that the container is running: `docker-compose ps`
- Check container logs: `docker logs <container-name>`

---

### Step 12: Test a Prometheus Query

Let's verify Prometheus is collecting metrics:

1. **Click "Graph"** in the top menu (or go to home)
2. In the query box at the top, type: `up{job="flask-app"}`
3. **Click "Execute"**
4. **Click the "Graph" tab** (next to "Table")

**You should see:**
- A line graph
- The value should be **1** (meaning the app is up)
- If you hover over the line, you'll see the value

**Try another query:**
- Type: `cpu_usage_percent`
- Click "Execute"
- You should see the CPU usage of your Flask app!

✅ **If queries work, Prometheus is collecting metrics correctly!**

---

### Step 13: Check Alert Rules

1. **Click "Alerts"** in the top menu
2. You should see your 3 alert rules:
   - **ServiceDown** (inactive/green)
   - **HighCPUUsage** (inactive/green)
   - **HighMemoryUsage** (inactive/green)

**All should be green (inactive) because nothing is wrong yet!**

We'll test these alerts later in the Failure Simulation section.

---

## PART 8: CONFIGURE GRAFANA

### Step 14: Access Grafana

Open your browser and go to:
```
http://localhost:3000
```

**Login screen will appear:**
- **Username**: `admin`
- **Password**: `admin`

**After login, Grafana may ask you to change the password:**
- You can change it or click "Skip" for now

✅ **You're now in Grafana!**

---

### Step 15: Add Prometheus as a Data Source

This tells Grafana where to get its data from.

**1. Click the ☰ menu** (hamburger icon, top left - the three horizontal lines)

**2. Navigate to: Connections → Data sources**
   - In the left sidebar, look for "Connections"
   - Click on it
   - Then click "Data sources"

**3. Click "Add data source"** (blue button)

**4. Select "Prometheus"** from the list
   - It should be near the top
   - Has an orange flame logo

**5. Configure the connection:**
   - **Name**: Leave as "Prometheus"
   - **URL**: Enter exactly: `http://prometheus:9090`
   
   ⚠️ **Important:** Use `http://prometheus:9090` (not `localhost`)
   - We use the container name, not localhost
   - This is Docker networking magic!

**6. Scroll to the bottom and click "Save & Test"**

**Expected result:**
- Green checkmark ✅
- Message: "Successfully queried the Prometheus API"

✅ **If you see green, the connection works!**

**If you see an error:**
- Double-check the URL is exactly: `http://prometheus:9090`
- Make sure Prometheus is running: `docker-compose ps`
- Try clicking "Save & Test" again

---

### Step 16: Import Node Exporter Dashboard

Let's import a pre-built dashboard that shows system metrics!

**1. Click the ☰ menu → Dashboards**

**2. Click "New" → "Import"** (buttons at the top right)

**3. In the "Import via grafana.com" field:**
   - Type: `1860`
   - Click "Load"

**4. On the import screen:**
   - **Name**: Node Exporter Full (already filled in)
   - **Folder**: Dashboards (default is fine)
   - **Prometheus**: Select "Prometheus" from the dropdown at the bottom

**5. Click "Import"**

**🎉 You should now see a beautiful dashboard!**

The dashboard shows:
- CPU usage
- Memory usage
- Disk I/O
- Network traffic
- System load
- And much more!

**All the graphs should have data flowing in.**

✅ **Take a moment to explore this dashboard!**

---

### Step 17: Create Custom Dashboard for Flask App

Now let's build our own dashboard to monitor the Flask application!

**1. Click the ☰ menu → Dashboards**

**2. Click "New" → "New Dashboard"**

**3. Click "Add visualization"**

**4. Select "Prometheus"** as the data source

---

#### Panel 1: App Status

This panel shows if the Flask app is up or down.

**In the query editor at the bottom:**

1. **Click on "Code"** button (top right of query section)
2. In the query box, type exactly: `up{job="flask-app"}`
3. **Click "Run queries"** (blue button, bottom right)
4. You should see the value **1** appear

**Configure the panel (right sidebar):**

1. **Panel options → Title**: Change "Panel Title" to `App Status`

2. **Visualization**: Click the dropdown at top right
   - Change from "Time series" to **"Stat"**

3. **Standard options → Thresholds** (scroll down on right side):
   - Click on the **Base** threshold
   - Change color to **Red** (🔴)
   - Click "+ Add threshold"
   - Set value to `1`
   - Change color to **Green** (🟢)

**What this does:**
- When value = 0 (app down) → Red
- When value = 1 (app up) → Green

**4. Click "Apply"** (top right, blue button)

✅ **You should see a green "1" on your dashboard!**

---

#### Panel 2: CPU Usage

**1. Click "Add" → "Visualization"** (top right)

**2. Select "Prometheus"**

**3. In the query box:**
   - Click "Code" button
   - Type: `cpu_usage_percent`
   - Click "Run queries"

**4. Configure the panel:**
   - **Title**: Change to `CPU Usage %`
   - **Visualization**: Keep as "Time series" (shows changes over time)

**5. Click "Apply"**

✅ **You should see a line graph showing CPU usage!**

---

#### Panel 3: Memory Usage

**1. Click "Add" → "Visualization"**

**2. Select "Prometheus"**

**3. Query:**
   - Type: `memory_usage_percent`
   - Click "Run queries"

**4. Configure:**
   - **Title**: `Memory Usage %`
   - **Visualization**: "Time series" or "Gauge" (try both!)

**5. Click "Apply"**

✅ **Now you have three panels showing app status, CPU, and memory!**

---

### Step 18: Save Your Dashboard

**1. Click the 💾 Save icon** (top right, looks like a floppy disk)

**2. Give it a name:**
   - Type: `Flask App Monitoring`

**3. Click "Save"**

🎉 **Your custom dashboard is now saved!**

---

## PART 9: TEST THE MONITORING SYSTEM

This is the **most important part** for SRE! We need to verify that our monitoring actually works when things go wrong.

---

### Test 1: Service Downtime Detection

Let's intentionally break our app and see if monitoring catches it!

**Step 1: Stop the Flask application**

Open your terminal:

```bash
docker stop flask-app
```

**Step 2: Wait and observe** (set a timer for 60 seconds)

**After 30-45 seconds, check Prometheus:**

1. Go to: http://localhost:9090/targets
   - Find the `flask-app` target
   - **It should be RED (DOWN)** 🔴
   - Error message: "connection refused"

2. Go to: http://localhost:9090/alerts
   - Watch the "ServiceDown" alert
   - It will go through these stages:
     - **Green (Inactive)** → Everything fine
     - **Orange (Pending)** → App is down, waiting 30s
     - **Red (Firing)** → Alert is active! 🚨

**Step 3: Check Grafana**

Go to your Flask App Monitoring dashboard:
- The "App Status" panel should show **0** (RED) 🔴
- CPU and Memory panels will show "No data" (app is stopped)

📸 **Take a screenshot!** This proves your monitoring works.

**Step 4: Restart the application**

```bash
docker start flask-app
```

**Wait 30 seconds, then check:**
- Prometheus targets: flask-app should be **GREEN (UP)** 🟢
- Prometheus alerts: ServiceDown should be **GREEN (Inactive)**
- Grafana: App Status should be **1 (GREEN)** 🟢

✅ **Success! Your monitoring detected a real failure!**

---

### Test 2: High CPU Load Simulation

Let's trigger the CPU alert!

**Step 1: Enter the Flask container**

```bash
docker exec -it flask-app bash
```

You're now inside the container!

**Step 2: Install stress testing tool**

```bash
apt-get update
apt-get install -y stress
```

**Step 3: Generate CPU load**

```bash
stress --cpu 2 --timeout 120s
```

This will max out 2 CPU cores for 2 minutes.

**Step 4: Observe in real-time**

**In Grafana:**
- Open your Flask App Monitoring dashboard
- Watch the CPU Usage % panel spike up! 📈
- The graph should show values jumping to 80-100%

**In Prometheus (after ~1 minute):**
- Go to: http://localhost:9090/alerts
- The "HighCPUUsage" alert should:
  - Turn **Orange (Pending)** after sustained high CPU
  - Turn **Red (Firing)** after 1 minute

📸 **Take a screenshot of the high CPU graph!**

**Step 5: Exit the container**

After the stress test finishes (or press Ctrl+C to stop it):

```bash
exit
```

✅ **You've validated that CPU monitoring works!**

---

### Test 3: Verify All Metrics are Flowing

Let's make sure everything is being collected:

**1. In Prometheus, try these queries:**

```
up{job="flask-app"}           # Should be 1
cpu_usage_percent             # Should show current CPU
memory_usage_percent          # Should show current memory
node_cpu_seconds_total        # System CPU time
node_memory_MemAvailable_bytes # System memory
```

**2. In Grafana, check both dashboards:**
- Node Exporter Full - All panels should have data
- Flask App Monitoring - All three panels working

✅ **If all queries return data, your monitoring is fully operational!**

---

## PART 10: UNDERSTANDING WHAT YOU BUILT

### How It All Works Together

Let's break down what's happening behind the scenes:

**1. Metric Collection (Every 15 seconds):**
```
Prometheus → Scrapes → Flask App (/metrics)
                     → Node Exporter (/metrics)
                     → Itself (self-monitoring)
```

**2. Data Storage:**
```
Prometheus stores metrics in time-series database
Each metric has: name, value, timestamp, labels
Example: cpu_usage_percent{job="flask-app"} = 23.5 at 2025-01-15 10:30:45
```

**3. Alerting:**
```
Prometheus evaluates rules every 10s
If condition met for specified duration → Alert fires
Example: up{job="flask-app"} == 0 for 30s → ServiceDown fires
```

**4. Visualization:**
```
Grafana → Queries Prometheus → Gets time-series data → Renders graphs
User sees beautiful dashboards with real-time updates
```

---

### Key Concepts Explained

#### What is a Metric?

A metric is a **numerical measurement** over time. Examples:
- CPU usage: 45.2%
- Memory used: 2.1 GB
- Requests per second: 150
- App up/down: 1 or 0

#### What is a Time-Series?

A sequence of measurements over time:
```
10:00:00 → CPU: 20%
10:00:15 → CPU: 25%
10:00:30 → CPU: 30%
10:00:45 → CPU: 28%
```

This lets us see trends, spikes, and patterns.

#### What is Scraping?

Prometheus **pulls** metrics from targets (it doesn't push):
```
Every 15 seconds:
Prometheus → HTTP
