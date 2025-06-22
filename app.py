from flask import Flask, jsonify, send_from_directory, request # Make sure 'request' is here
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'gmc_sierra_progress.db'
HTML_DIR = os.path.dirname(os.path.abspath(__file__))

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

@app.route('/')
def serve_html():
    # Make sure the filename matches your actual HTML file name
    return send_from_directory(HTML_DIR, 'gmc_sierra_rebuild_guide fuel injection full plan.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, status, cost FROM tasks ORDER BY id") # Order by ID for consistent display
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

    # The try...except...finally block must be properly indented inside the function
    try:
        # Build the update query dynamically based on what's provided
        updates = []
        params = []
        if status is not None:
            updates.append("status = ?")
            params.append(status)
        if cost is not None:
            updates.append("cost = ?")
            params.append(float(cost)) # Ensure cost is stored as a float

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

# This is the new function, placed after the update_task function
@app.route('/api/total_cost', methods=['GET'])
def get_total_cost():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(cost) FROM tasks")
    total_cost = cursor.fetchone()[0] # fetchone() returns a tuple, get the first element
    conn.close()
    # Ensure it's a float, default to 0.0 if None (no costs yet)
    return jsonify({'total_cost': total_cost if total_cost is not None else 0.0})

if __name__ == '__main__':
    app.run(debug=True)