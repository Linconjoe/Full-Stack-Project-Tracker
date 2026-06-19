import sqlite3

def add_fuel_system_tasks():
    # Connect to your existing SQLite database
    # (Adjust the database name if your Flask app uses a different one)
    conn = sqlite3.connect('gmc_sierra_progress.db')
    cursor = conn.cursor()

    # The high-pressure fuel system tasks required for the Edelbrock Pro-Flo 4 & Smeding 383
    new_tasks = [
        ("Source: Quantum/Walbro 255LPH High-Pressure In-Tank Fuel Pump (OBS Direct Fit)", "Not Started", 130.00),
        ("Source: -6AN PTFE Fuel Line Kit (25ft) with Fittings (Feed & Return)", "Not Started", 180.00),
        ("Source: EFI Quick Disconnect Fittings for factory sending unit to -6AN", "Not Started", 45.00),
        ("Source: High-Pressure Inline Fuel Filter (10 Micron)", "Not Started", 60.00),
        ("Install: Drop fuel tank, clean, and install new 255LPH high-pressure pump", "Not Started", 0.00),
        ("Install: Route -6AN PTFE feed and return lines along frame rail away from exhaust", "Not Started", 0.00),
        ("Install: Plumb -6AN lines to Edelbrock Pro-Flo 4 fuel rails and set base pressure to 58 PSI", "Not Started", 0.00)
    ]

    # Insert tasks into the database
    for description, status, cost in new_tasks:
        cursor.execute('''
            INSERT INTO tasks (description, status, cost)
            VALUES (?, ?, ?)
        ''', (description, status, cost))

    conn.commit()
    conn.close()
    print("Successfully added the EFI high-pressure fuel system tasks to the project database!")

if __name__ == '__main__':
    add_fuel_system_tasks()