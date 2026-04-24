from flask import Flask, render_template, request, jsonify
import json, os, uuid
from datetime import datetime

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
PROFILES_FILE = os.path.join(DATA_DIR, 'profiles.json')


def load_profiles():
    if not os.path.exists(PROFILES_FILE):
        return {}
    with open(PROFILES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_profiles(profiles):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PROFILES_FILE, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    return jsonify(load_profiles())


@app.route('/api/profiles', methods=['POST'])
def add_profile():
    data = request.json
    required = ['firstName', 'lastName', 'birthDay', 'birthMonth', 'birthYear']
    for field in required:
        if field not in data:
            return jsonify({'error': f'שדה חסר: {field}'}), 400
    profiles = load_profiles()
    pid = str(uuid.uuid4())[:8]
    profiles[pid] = {
        **data,
        'id': pid,
        'createdAt': datetime.now().isoformat()
    }
    save_profiles(profiles)
    return jsonify(profiles[pid]), 201


@app.route('/api/profiles/<pid>', methods=['PUT'])
def update_profile(pid):
    data = request.json
    profiles = load_profiles()
    if pid not in profiles:
        return jsonify({'error': 'פרופיל לא נמצא'}), 404
    profiles[pid].update(data)
    save_profiles(profiles)
    return jsonify(profiles[pid])


@app.route('/api/profiles/<pid>', methods=['DELETE'])
def delete_profile(pid):
    profiles = load_profiles()
    if pid not in profiles:
        return jsonify({'error': 'פרופיל לא נמצא'}), 404
    del profiles[pid]
    save_profiles(profiles)
    return jsonify({'success': True})


if __name__ == '__main__':
    import webbrowser, threading
    def open_browser():
        webbrowser.open('http://localhost:5000')
    threading.Timer(1.2, open_browser).start()
    app.run(debug=False, port=5000)
