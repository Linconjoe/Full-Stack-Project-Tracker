import sqlite3

def add_task(description):
    conn = sqlite3.connect('gmc_sierra_progress.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (description, status) VALUES (?, ?)", (description, 'Not Started'))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    print(f"Task '{description}' added with ID: {task_id}")
    return task_id

if __name__ == "__main__":
    tasks_to_add = [
        "Engine Rebuild",
        "Replace Side Marker Lights",
        "Replace Front Lights",
        "Replace Grill",
        "Replace Interior Door Parts",
        "Fix Rear Tailgate",
        "Weather Seal Around Windows"
        # Add other tasks here if you like
    ]

    for task in tasks_to_add:
        add_task(task)