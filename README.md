# GMC Project Plan: 1990 GMC Sierra 350 EFI Engine Rebuild to 300-325 HP
This report presents a comprehensive project plan for rebuilding a 1990 GMC Sierra's 350 cubic inch (5.7L) engine, now upgraded to **Electronic Fuel Injection (EFI) via a Throttle Body Injection (TBI) system**, with the objective of reliably achieving 300-325 horsepower. The plan meticulously details strategic component upgrades, emphasizes precise assembly techniques, and outlines critical tuning procedures. A core principle of this project is the exclusive use of new or factory-refurbished components, ensuring enhanced performance while maintaining the integrity and longevity of the vehicle, especially for **reliable long-distance trips (6-7 hours)**.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

-   **Maintenance Tracking:** Log and view service history, upcoming maintenance, and repair details.
-   **Performance Monitoring:** Record fuel efficiency, mileage, and other performance metrics over time.
-   **Customization Log:** Document modifications, upgrades, and accessories added to the vehicle.
-   **Data Visualization:** (Planned) Interactive charts and graphs for insights into vehicle data.
-   **Search & Filter:** Easily find specific records based on various criteria.

## Installation

To get this project up and running on your local machine, follow these steps:

### Prerequisites

* Python 3.8+
* pip (Python package installer)
* Git

### Steps

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:Linconjoe/gmc_sierra_pro_project.git
    cd gmc_sierra_pro_project
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

    ## Usage

### Running the Application

After installation, you can start the main application script:

```bash
# Make sure your virtual environment is active
python src/main_app.py

## Project Structure

.
├── src/                 # Main application source code
│   ├── core/            # Core logic and data models
│   ├── modules/         # Feature-specific modules
│   └── main_app.py      # Main entry point
├── data/                # Data storage (e.g., SQLite DB, CSVs)
├── docs/                # Documentation files (if any)
├── tests/               # Unit and integration tests
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── .gitignore           # Files/directories ignored by Git

