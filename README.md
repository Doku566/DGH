# IT Inventory System (Flask Version)

This is a web-based IT Inventory System built with Python and the Flask framework. It allows users to register, login, and manage hardware and software assets.

## Prerequisites

*   Python 3.7+
*   `pip` (Python package installer)
*   `venv` (for creating virtual environments, usually included with Python)

## Setup Instructions

1.  **Clone the Repository (Conceptual)**
    *   If this project were on a Git hosting service (like GitHub), you would clone it using:
        ```bash
        git clone <repository_url>
        cd <repository_directory>
        ```
    *   For now, ensure you have all the project files in a local directory.

2.  **Create and Activate a Virtual Environment**
    *   It's highly recommended to use a virtual environment to manage project dependencies.
    *   Navigate to the project's root directory in your terminal.

    *   **On macOS and Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

    *   **On Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   You should see `(venv)` prefixed to your terminal prompt, indicating the virtual environment is active.

3.  **Install Dependencies**
    *   With the virtual environment activated, install the required packages using the `requirements.txt` file:
        ```bash
        pip install -r requirements.txt
        ```

## Database Initialization

The application uses SQLite as its database.
*   The database file (`inventory.db`) will be automatically created inside an `instance` folder within the project root when you first run the application.
*   The necessary tables will also be created automatically based on the models defined in `app/models.py` due to the `db.create_all()` command in the application factory.

## Running the Application

1.  **Set Flask Environment Variables**
    *   Open your terminal (with the virtual environment activated).
    *   You need to tell Flask where to find the application instance. Our entry point is `autoapp.py`.

    *   **On macOS and Linux:**
        ```bash
        export FLASK_APP=autoapp.py
        export FLASK_ENV=development # Optional: enables debug mode and other dev features
        ```

    *   **On Windows (Command Prompt):**
        ```bash
        set FLASK_APP=autoapp.py
        set FLASK_ENV=development
        ```

    *   **On Windows (PowerShell):**
        ```bash
        $env:FLASK_APP = "autoapp.py"
        $env:FLASK_ENV = "development"
        ```
    *   *Note: `FLASK_ENV=development` enables debug mode. For production, this should be `production`.*

2.  **Run the Flask Development Server**
    *   Once the environment variables are set, run the application using:
        ```bash
        flask run
        ```

3.  **Access the Application**
    *   Open your web browser and navigate to:
        [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Creating an Initial User

*   Once the application is running, the first step is to create a user account.
*   Navigate to the registration page: [http://127.0.0.1:5000/auth/register](http://127.0.0.1:5000/auth/register)
*   Fill out the registration form and submit it. You can then log in with your new credentials.

## Project Structure

A brief overview of the project's layout:

```
.
├── app/                  # Main application package
│   ├── static/           # Static files (CSS, JS, images)
│   │   └── css/
│   │       └── style.css
│   ├── templates/        # HTML templates
│   │   ├── auth/         # Authentication-related templates (login, register)
│   │   └── main/         # Main app templates (dashboard, add item, inventory list)
│   │   └── base.html     # Base template for others to extend
│   ├── __init__.py       # Application factory (create_app)
│   ├── auth.py           # Authentication blueprint, routes, and logic
│   ├── forms.py          # WTForms definitions
│   ├── main.py           # Main application blueprint and routes (inventory, add item)
│   └── models.py         # SQLAlchemy database models
├── instance/             # Instance folder (e.g., for SQLite DB file, not version controlled by default)
│   └── inventory.db      # SQLite database file (created automatically)
├── venv/                 # Python virtual environment (if created with this name)
├── autoapp.py            # Flask application entry point for `flask run`
├── requirements.txt      # Python package dependencies
└── README.md             # This file
```

This `README.md` provides a comprehensive guide for setting up and running the Flask application locally.
