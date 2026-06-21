from flask import Flask, render_template, jsonify, request
import subprocess
import os

app = Flask(__name__)

SIMULATOR_PATH = "./simulator"
TRACES_DIR = "traces"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/traces')
def get_traces():
    # Return list of available trace files
    traces = [f for f in os.listdir(TRACES_DIR) 
              if f.endswith('.trace')]
    return jsonify(traces)

@app.route('/api/run', methods=['POST'])
def run_simulation():
    data = request.get_json()
    trace_file = data.get('trace', 'traces/realistic.trace')
    capacity = data.get('capacity', 8)

    try:
        result = subprocess.run(
            [SIMULATOR_PATH, trace_file, str(capacity)],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500

        # Parse CSV output from C++
        policies = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split(',')
            if len(parts) == 4:
                policies.append({
                    'policy': parts[0],
                    'hits': int(parts[1]),
                    'misses': int(parts[2]),
                    'hitRate': float(parts[3])
                })

        return jsonify({
            'trace': trace_file,
            'capacity': capacity,
            'results': policies
        })

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Simulation timed out'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/step', methods=['POST'])
def step_simulation():
    data = request.get_json()
    trace = data.get('trace', [])
    capacity = data.get('capacity', 8)
    index = data.get('index', 0)

    if index >= len(trace):
        return jsonify({'done': True})

    address = trace[index]

    return jsonify({
        'done': False,
        'index': index,
        'address': address,
        'next_index': index + 1
    })

if __name__ == '__main__':
    app.run(debug=True)