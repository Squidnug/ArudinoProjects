import time
from threading import Thread, Lock
from flask import Flask, jsonify

app = Flask(__name__)

latest_sound = None
sound_lock = Lock()


def updateSound(sound_value):
    global latest_sound

    with sound_lock:
        latest_sound = sound_value


@app.route("/")
def dashboard():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Sound Dashboard</title>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        body {
            background: #111827;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 30px;
        }

        .card {
            background: #1f2937;
            max-width: 900px;
            margin: 20px auto;
            padding: 25px;
            border-radius: 15px;
        }

        #soundValue {
            font-size: 70px;
            font-weight: bold;
        }

        #status {
            font-size: 24px;
            margin: 15px;
        }

        .chart-container {
            height: 400px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            max-width: 900px;
            margin: 20px auto;
        }

        .stat-box {
            background: #1f2937;
            padding: 20px;
            border-radius: 15px;
        }

        .stat-label {
            font-size: 14px;
            color: #9ca3af;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }

        .stat-value {
            font-size: 36px;
            font-weight: bold;
        }

        .stat-sub {
            font-size: 13px;
            color: #9ca3af;
            margin-top: 6px;
        }

        .peak-value {
            color: #f87171;
        }

        .avg-value {
            color: #60a5fa;
        }

        .min-value {
            color: #34d399;
        }

        .legend-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }

        .legend-table th {
            text-align: left;
            padding: 10px 15px;
            color: #9ca3af;
            text-transform: uppercase;
            font-size: 13px;
            letter-spacing: 1px;
            border-bottom: 1px solid #374151;
        }

        .legend-table td {
            text-align: left;
            padding: 12px 15px;
            font-size: 18px;
            border-bottom: 1px solid #374151;
        }

        .legend-table tr:last-child td {
            border-bottom: none;
        }

        .legend-db {
            font-weight: bold;
        }
    </style>
</head>

<body>
    <h1>Live Sound Monitor</h1>

    <div class="card">
        <div>Current sound level</div>
        <div id="soundValue">--</div>
        <div id="status">Waiting for data</div>
    </div>

    <div class="stats-grid">
        <div class="stat-box">
            <div class="stat-label">Peak Level</div>
            <div class="stat-value peak-value" id="peakValue">--</div>
            <div class="stat-sub" id="peakTime">no data yet</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Average Level</div>
            <div class="stat-value avg-value" id="avgValue">--</div>
            <div class="stat-sub" id="avgSub">since page load</div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Lowest Level</div>
            <div class="stat-value min-value" id="minValue">--</div>
            <div class="stat-sub" id="minSub">since page load</div>
        </div>
    </div>

    <div class="card chart-container">
        <canvas id="soundChart"></canvas>
    </div>

    <div class="card">
        <h2 style="margin-top: 0;">Sound Level Reference</h2>
        <table class="legend-table">
            <thead>
                <tr>
                    <th>dB</th>
                    <th>Level</th>
                    <th>Data Number</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="legend-db">65</td>
                    <td>Normal</td>
                    <td>5</td>
                </tr>
                <tr>
                    <td class="legend-db">75</td>
                    <td>Loud</td>
                    <td>12</td>
                </tr>
                <tr>
                    <td class="legend-db">85</td>
                    <td>Extremely Loud</td>
                    <td>30</td>
                </tr>
            </tbody>
        </table>
    </div>

    <script>
        const soundValue = document.getElementById("soundValue");
        const status = document.getElementById("status");

        const peakValueEl = document.getElementById("peakValue");
        const peakTimeEl = document.getElementById("peakTime");
        const avgValueEl = document.getElementById("avgValue");
        const minValueEl = document.getElementById("minValue");

        let peak = null;
        let peakTimestamp = null;
        let minVal = null;
        let total = 0;
        let count = 0;

        const chart = new Chart(
            document.getElementById("soundChart"),
            {
                type: "line",

                data: {
                    labels: [],
                    datasets: [{
                        label: "Sound Level",
                        data: [],
                        borderWidth: 2,
                        pointRadius: 0
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: false,

                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            }
        );

        function updatePeakTimeDisplay() {
            if (peakTimestamp === null) {
                return;
            }

            const secondsAgo = Math.floor((Date.now() - peakTimestamp) / 1000);

            if (secondsAgo < 60) {
                peakTimeEl.textContent = secondsAgo + "s ago";
            } else if (secondsAgo < 3600) {
                peakTimeEl.textContent = Math.floor(secondsAgo / 60) + "m ago";
            } else {
                peakTimeEl.textContent = Math.floor(secondsAgo / 3600) + "h ago";
            }
        }

        async function getSoundData() {
            try {
                const response = await fetch("/data");
                const data = await response.json();

                if (data.sound === null) {
                    return;
                }

                const sound = Number(data.sound);

                soundValue.textContent = sound;
                
                if (sound > 25) {
                    status.textContent = "85dB+";
                } else if (sound > 12) {
                    status.textContent = "75dB+";
                } else {
                    status.textContent = ">65dB";
                }

                // update peak
                if (peak === null || sound > peak) {
                    peak = sound;
                    peakTimestamp = Date.now();
                    peakValueEl.textContent = peak;
                }

                // update min
                if (minVal === null || sound < minVal) {
                    minVal = sound;
                    minValueEl.textContent = minVal;
                }

                // update average
                total += sound;
                count += 1;
                avgValueEl.textContent = (total / count).toFixed(1);

                updatePeakTimeDisplay();

                chart.data.labels.push(
                    new Date().toLocaleTimeString()
                );

                chart.data.datasets[0].data.push(sound);

                if (chart.data.labels.length > 100) {
                    chart.data.labels.shift();
                    chart.data.datasets[0].data.shift();
                }

                chart.update("none");

            } catch (error) {
                status.textContent = "Dashboard connection error";
            }
        }

        setInterval(getSoundData, 200);
        setInterval(updatePeakTimeDisplay, 1000);
        getSoundData();
    </script>
</body>
</html>
"""


@app.route("/data")
def data():
    with sound_lock:
        sound_value = latest_sound

    try:
        sound_number = int(sound_value)
    except (TypeError, ValueError):
        sound_number = None

    return jsonify(
        sound=sound_number,
        timestamp=time.time()
    )


def runDashboard():
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )


def startDash():
    dashboard_thread = Thread(
        target=runDashboard,
        daemon=True
    )

    dashboard_thread.start()
