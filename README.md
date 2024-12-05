# Unsecure project for Cyber Security Base Project 1

# Startup Instructions

[!NOTE]
The project uses SQLite, so no need for setting up your own postgres and what not. The database is initialized automatically.

1. **Install Poetry**: If you haven't already, install Poetry for your operating system by following the instructions at [Poetry Installation](https://python-poetry.org/docs/#installation).

2. **Install Dependencies**: Navigate to your project directory and install the dependencies specified in by running:

    ```bash
    poetry install
    ```

3. **Activate the Virtual Environment**: Activate the virtual environment created by Poetry:

    ```bash
    poetry shell
    ```

4. **Run the Flask Application**: Start your Flask application by running:

    ```bash
    flask run
    ```

5. **Access the Application**: Open your web browser and go to `http://127.0.0.1:5000` to see your Flask app in action.

## Vulnerability 1.

### A9:2017-Using Components with Known Vulnerabilities

By using an outdated version of Werkzeug python library, it is vulnerable to a vulnerability "Werkzeug debugger vulnerable to remote execution when interacting with attacker controlled domain"
https://github.com/pallets/werkzeug/security/advisories/GHSA-2g68-c3qc-8985  
Appropriate fix would be to update this dependency in `pyproject.toml` file, which instructs Poetry to get an appropriate version of the dependency.

To update this: change the Werkzeug version in `pyproject.toml` to

```
werkzeug = "^3.1.0"
```

Then run

```bash
poetry update
```

## Vulnerability 2.

### A2:2017-Broken Authentication

By checking admin priveledges from url parameter if link is `/admin?is_admin=true`, this creates a vulnerability for broken authentication. As some malicous party could compromise and see all the notes of all users.

Appropriate fix would be to check if user has priveledges based on data from the database.
