from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import psutil
import datetime

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def dashboard():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    uptime_seconds = datetime.datetime.now().timestamp() - psutil.boot_time()
    uptime = str(datetime.timedelta(seconds=int(uptime_seconds)))

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>buddahserver dashboard</title>
        <meta http-equiv="refresh" content="10">
        <style>
            body {{
                font-family: monospace;
                background: #1a1a2e;
                color: #eee;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }}
            .card {{
                background: #16213e;
                border: 1px solid #0f3460;
                border-radius: 12px;
                padding: 40px;
                min-width: 400px;
            }}
            h1 {{ color: #e94560; margin-top: 0; }}
            .stat {{ margin: 20px 0; }}
            .label {{
                color: #888;
                font-size: 12px;
                text-transform: uppercase;
            }}
            .value {{
                font-size: 28px;
                font-weight: bold;
                color: #4fc3f7;
            }}
            .bar {{
                background: #0f3460;
                border-radius: 4px;
                height: 8px;
                margin-top: 8px;
            }}
            .bar-fill {{
                background: #e94560;
                border-radius: 4px;
                height: 8px;
            }}
            .timestamp {{
                color: #555;
                font-size: 11px;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>⚡ buddahserver</h1>
            <div class="stat">
                <div class="label">CPU Usage</div>
                <div class="value">{cpu}%</div>
                <div class="bar"><div class="bar-fill" style="width:{cpu}%"></div></div>
            </div>
            <div class="stat">
                <div class="label">Memory Usage</div>
                <div class="value">{memory.percent}%</div>
                <div class="bar"><div class="bar-fill" style="width:{memory.percent}%"></div></div>
            </div>
            <div class="stat">
                <div class="label">Disk Usage</div>
                <div class="value">{disk.percent}%</div>
                <div class="bar"><div class="bar-fill" style="width:{disk.percent}%"></div></div>
            </div>
            <div class="stat">
                <div class="label">Uptime</div>
                <div class="value">{uptime}</div>
            </div>
            <div class="timestamp">Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} · Refreshes every 10 seconds</div>
        </div>
    </body>
    </html>
    """
    return html

@app.get("/api/stats")
def stats():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    uptime_seconds = datetime.datetime.now().timestamp() - psutil.boot_time()
    return {
        "cpu_percent": cpu,
        "memory_percent": memory.percent,
        "memory_total_gb": round(memory.total / (1024**3), 1),
        "memory_used_gb": round(memory.used / (1024**3), 1),
        "disk_percent": disk.percent,
        "disk_total_gb": round(disk.total / (1024**3), 1),
        "disk_used_gb": round(disk.used / (1024**3), 1),
        "uptime": str(datetime.timedelta(seconds=int(uptime_seconds)))
    }
