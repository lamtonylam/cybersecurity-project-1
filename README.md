# Unsecure project for Cyber Security Base Project 1

# Startup Instructions

> [!NOTE]
> The project uses SQLite, so no need for setting up your own postgres and what not. The database is initialized automatically.

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

To update this: change the Werkzeug version in `pyproject.toml` https://github.com/lamtonylam/cybersecurity-project-1/blob/e7527bf8c394a3f93973442e84bc2960f7422c9c/pyproject.toml#L12 to

```
werkzeug = "^3.1.0"
```

Then run

```bash
poetry update
```

## Vulnerability 2.

### A5:2017-Broken Access Control
https://github.com/lamtonylam/cybersecurity-project-1/blob/0692eb82a3ab90095f6c653a7d07812f38fc0096/app.py#L110
By checking admin priveledges from url parameter if link is `/admin?is_admin=true`, this creates a vulnerability for Broken Access Control. As some malicous party could compromise and see all the notes of all users.

Appropriate fix would be to check if user has priveledges based on data from the database.  
Uncomment the fix:
https://github.com/lamtonylam/cybersecurity-project-1/blob/0692eb82a3ab90095f6c653a7d07812f38fc0096/app.py#L113

## Vulnerability 3.

### A3:2017-Sensitive Data Exposure
https://github.com/lamtonylam/cybersecurity-project-1/blob/0692eb82a3ab90095f6c653a7d07812f38fc0096/db.py#L57
https://github.com/lamtonylam/cybersecurity-project-1/blob/0692eb82a3ab90095f6c653a7d07812f38fc0096/db.py#L58
https://github.com/lamtonylam/cybersecurity-project-1/blob/0692eb82a3ab90095f6c653a7d07812f38fc0096/db.py#L59

Not hashing passwords when registering users creates a vulnerability for sensitive data exposure.  
If an malicious party gains access to the database, they can immediately see all user passwords in plaintext mode.
This also creates a threat for inside organizations, as database admins can see all user passwords in their plain format.

Appropriate fix would be to hash user passwords with Werkzeug library.  
Uncomment the fix:
https://github.com/lamtonylam/cybersecurity-project-1/blob/0692eb82a3ab90095f6c653a7d07812f38fc0096/db.py#L65

## Vulnerability 4.

### A2:2017-Broken Authentication

Not checking registering users passwords against a list of most commonly used ie. unsafe passwords, it is vulnerable for malicious actors to brute force user's accounts by guessing passwords that are commonly used, like 12345678 or qwerty.

Appropriate fix would be to check registering password against most commonly used passwords.

## Vulnerability 5.

### A10:2017-Insufficient Logging & Monitoring

By not logging critical security events that happen on the website, such as failed login attempts, successful/failed registrations, and administrative page access, attackers can perform malicious activities without being detected.

Performing proper security incident investigations becomes nearly impossible without adequate logging records of user activities and system events. The lack of monitoring capabilities significantly impacts the ability to respond to and investigate security incidents in a timely manner.

The fix would be to implement logging using Python's logging framework.
