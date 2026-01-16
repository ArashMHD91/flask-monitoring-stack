from flask import Flask, jsonify
import psutil
import time

app = Flask(__name__)

# This is our health check endpoint
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time()
    }), 200

# Homepage
@app.route('/')
def home():
    return "Hello! I'm a simple monitored service! 👋"

# Metrics endpoint (Prometheus format)
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
