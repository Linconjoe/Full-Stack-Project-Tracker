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
    # Clear existing tasks to avoid duplicates if re-running without a fresh DB
    # You might want to remove this line if you have existing tasks you want to keep
    # and only add the new ones manually. For a full re-sync, it's useful.
    conn = sqlite3.connect('gmc_sierra_progress.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()
    print("Cleared existing tasks from the database.")


    tasks_to_add = [
        # New Engine Swap & MPFI Conversion Tasks
        "Phase 1: Original Engine Removal & Prep",
        "Phase 2: Crate Engine & MPFI Installation",
        "Phase 3: Supporting Systems & Driveline Reinforcement",
        "Phase 4: Initial Startup & Advanced MPFI Tuning",

        # Other Vehicle Tasks (remain the same)
        "Replace Side Marker Lights",
        "Replace Front Lights (Headlights/Turn Signals)",
        "Replace Grill",
        "Replace Interior Door Parts",
        "Fix Rear Tailgate (doesn't stay closed)",
        "Replace Weather Seal Around Windows"
    ]

    print("\nAdding new tasks to the database:")
    for task in tasks_to_add:
        add_task(task)

    print("\nAll specified tasks have been added/updated in the database.")