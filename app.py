from flask import Flask, jsonify, send_from_directory, request
import sqlite3
import os
import json
import base64
import requests

app = Flask(__name__)

# This is your correct database name!
DATABASE = 'gmc_sierra_progress.db'
HTML_DIR = os.path.dirname(os.path.abspath(__file__))

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

# Automatically ensure the UI state table exists when the server starts
def init_ui_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ui_state (
            element_id TEXT PRIMARY KEY,
            state_value TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Run the table creation
init_ui_db()

@app.route('/')
def serve_html():
    # Make sure the filename matches your actual HTML file name
    return send_from_directory(HTML_DIR, 'gmc_sierra_rebuild_guide fuel injection full plan.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, status, cost FROM tasks ORDER BY id") 
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(tasks)

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    status = data.get('status')
    cost = data.get('cost')

    conn = get_db()
    cursor = conn.cursor()

    try:
        updates = []
        params = []
        if status is not None:
            updates.append("status = ?")
            params.append(status)
        if cost is not None:
            updates.append("cost = ?")
            params.append(float(cost)) 

        if not updates:
            return jsonify({'message': 'No data provided for update'}), 400

        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        params.append(task_id)

        cursor.execute(query, tuple(params))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'message': 'Task not found'}), 404
        return jsonify({'message': 'Task updated successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'message': f'Error updating task: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/api/total_cost', methods=['GET'])
def get_total_cost():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(cost) FROM tasks")
    total_cost = cursor.fetchone()[0] 
    conn.close()
    return jsonify({'total_cost': total_cost if total_cost is not None else 0.0})

# ==========================================
# NEW ROUTES FOR CHECKBOXES & BUDGET
# ==========================================
@app.route('/api/ui_state', methods=['GET'])
def get_ui_state():
    """Fetches all saved checkbox, dropdown, and budget states."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT element_id, state_value FROM ui_state')
    rows = cursor.fetchall()
    conn.close()
    
    # Format the sqlite3.Row dictionaries back into a simple key:value JSON object
    return jsonify({row['element_id']: row['state_value'] for row in rows})

@app.route('/api/ui_state', methods=['POST'])
def update_ui_state():
    """Saves a checkbox, dropdown, or budget state instantly."""
    data = request.json
    element_id = data.get('element_id')
    state_value = data.get('state_value')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ui_state (element_id, state_value)
        VALUES (?, ?)
        ON CONFLICT(element_id) DO UPDATE SET state_value=excluded.state_value
    ''', (element_id, state_value))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})


# ==========================================
# AI MECHANIC ROUTE
# ==========================================
OLLAMA_API_URL = os.environ.get('OLLAMA_API_URL', 'http://127.0.0.1:11434')

def get_project_context():
    """Reads your HTML file to give the AI your specific project plan."""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'gmc_sierra_rebuild_guide fuel injection full plan.html')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            import re
            clean_text = re.sub(r'<[^>]+>', ' ', html_content)
            return clean_text[:8000] 
    except Exception as e:
        print(f"Could not load context: {e}")
        return "You are assisting with a 1990 GMC Sierra engine swap."

def ask_llama(prompt_text):
    """Sends a prompt to the local Llama 3.2 model with your custom context."""
    endpoint = f"{OLLAMA_API_URL}/api/generate"
    
    project_plan = get_project_context()
    
    system_instructions = f"""You are an expert master mechanic. You are helping execute this specific project plan:

{project_plan}

KEY PROJECT FACTS:
- EFI System: Edelbrock Pro-Flo 4 #35760 — pre-installed and baseline-tuned by Smeding Performance
- Pro-Flo 4 uses Bluetooth E-Tuner 4 app (iOS/Android) — NO CAN Bus, NO touchscreen tuner
- Pro-Flo 4 specs: 29 lb/hr injectors, 58 PSI fuel pressure, self-learning ECU, 450 HP rated
- There is NO ACES EFI system on this build. Do not reference ACES EFI or Wild Card in any response.
- Transmission: 4L80E with a standalone TCM (specific TCM brand TBD)

CRITICAL INSTRUCTIONS:
1. Treat any new numbers, budget updates, costs, or facts provided by the user in the chat as official and absolute truth.
2. If the user provides budget numbers, incorporate them directly into your response.
3. NEVER confuse "estimated costs" from the project plan with actual money spent.
4. ONLY count money as "spent" if the user explicitly tells you they purchased an item or states their "Actual Cost Spent".
5. If the user says their actual spent is $42.00, then their spent is EXACTLY $42.00, regardless of the estimates in the plan."""

    payload = {
        "model": "llama3.2",
        "prompt": prompt_text,
        "system": system_instructions,
        "temperature": 0.1,
        "stream": False
    }
    
    try:
        response = requests.post(endpoint, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "No response generated.")
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"

@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    data = request.json
    user_question = data.get('question')
    
    if not user_question:
        return jsonify({"error": "No question provided"}), 400
        
    ai_answer = ask_llama(user_question)
    return jsonify({"answer": ai_answer})

# ==========================================
# WIRING DIAGRAM ROUTES
# ==========================================
DIAGRAMS_DIR = os.path.join(HTML_DIR, 'Electrical diagrams')

@app.route('/diagrams')
def diagrams_page():
    return send_from_directory(HTML_DIR, 'diagrams.html')

@app.route('/diagrams/img/<filename>')
def serve_diagram_image(filename):
    return send_from_directory(DIAGRAMS_DIR, filename)

@app.route('/api/diagrams')
def get_diagrams():
    index_path = os.path.join(HTML_DIR, 'diagram_index.json')
    with open(index_path) as f:
        return jsonify(json.load(f))

@app.route('/api/ask_diagram', methods=['POST'])
def ask_diagram():
    data = request.json
    fig_num = int(data.get('fig_num', 1))
    question = data.get('question', '')

    img_path = os.path.join(DIAGRAMS_DIR, f'fig_{fig_num:02d}.gif')
    with open(img_path, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()

    endpoint = f"{OLLAMA_API_URL}/api/generate"

    # Try llava (vision model) first
    try:
        payload = {
            "model": "llava",
            "prompt": f"You are an expert automotive electrician analyzing a GM truck wiring diagram. {question}",
            "images": [img_b64],
            "stream": False
        }
        response = requests.post(endpoint, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json().get("response", "No response generated.")
        return jsonify({"answer": result, "model": "llava (vision)"})
    except Exception:
        pass

    # Fall back to llama3.2 text with diagram metadata
    index_path = os.path.join(HTML_DIR, 'diagram_index.json')
    with open(index_path) as f:
        diagrams = json.load(f)
    meta = next((d for d in diagrams if d['fig'] == fig_num), {})
    context = f"Diagram: Fig {fig_num} — {meta.get('title','Unknown')} | Years: {meta.get('years','')} | Engines: {', '.join(meta.get('engines',[]))} | Trans: {meta.get('trans','')}"
    answer = ask_llama(f"[Wiring Diagram Context] {context}\n\nUser question: {question}\n\nNote: You cannot see the image directly. Answer based on your knowledge of GM truck wiring for this diagram type.")
    return jsonify({"answer": answer, "model": "llama3.2 (text — install llava for vision queries)"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)