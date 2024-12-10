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

Exploiting this vulnerability could enable attackers to execute arbitrary code on the server, potentially gaining unauthorized access to sensitive data or further compromising the application.

Appropriate fix would be to update this dependency in `pyproject.toml` file, which instructs Poetry to get an appropriate version of the dependency. Keeping dependencies up-to-date should be a routine part of the development cycle to mitigate risks stemming from vulnerable components. Regular security scans and audits of software dependencies can help to identify outdated or vulnerable dependencies, one of these is for example dependabot which is built in Github. One of the neat things about enabling dependabot is that it can create automatic pull requests to update the dependencies, requiring only accepting the pull request on the project.

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
By checking admin priveledges from url parameter if link is `/admin?is_admin=true`, this creates a vulnerability for Broken Access Control. As some malicous party could compromise and see all the notes of all users. This is a significant flaw, as it relies on client-controlled input, which can be manipulated by an attacker to bypass access restrictions. Relying on client-side data for access control decisions violates the principle of secure server-side validation.

The security failure lies in trusting the user-side-input for determining user priviledges, which is totally unsecure.

Appropriate fix would be to check if user has priveledges based on data from the database.  
Uncomment the fix:
https://github.com/lamtonylam/cybersecurity-project-1/blob/0692eb82a3ab90095f6c653a7d07812f38fc0096/app.py#L113

## Vulnerability 3.

### A3:2017-Sensitive Data Exposure

https://github.com/lamtonylam/cybersecurity-project-1/blob/0692eb82a3ab90095f6c653a7d07812f38fc0096/db.py#L57
https://github.com/lamtonylam/cybersecurity-project-1/blob/0692eb82a3ab90095f6c653a7d07812f38fc0096/db.py#L58
https://github.com/lamtonylam/cybersecurity-project-1/blob/0692eb82a3ab90095f6c653a7d07812f38fc0096/db.py#L59

Not hashing passwords when registering users creates a vulnerability for sensitive data exposure.

From an extenral perpective, if a database containing passwords stored in plaintext would be breached, for example by some other methods like SQL injections, network intrusions or perhaps by hosting service provider's mistake. The attacker would have immediate access to user's passwords in a plaintext format. Allowing attackers immediate access to passwords and credentials.

And the risk exists also from within organizations. Database administrators, software developers, and other internal empyloyees having access to database. Could potentially view, copy or misuse the passwords in a plaintext form, instead of seeing hashed values.

If plaintext passwords were to have been stolen from database, there would essentially be no time in between for the attack to have happened and the passwords to have been in use my threat actors.
As the attackers have no need to decrypt them.

With some users reusing passwords between different services such as emails and social media platforms. This issue becomes more magnified in the context of a user, when the attacker can with a single plaintext password gain access to other important services too.

For example with the default hashing by Werkzeug library is by scrypt hashing.
This prolongs cracking of individual passwords, even with relatively easy passwords, cracking it would take months to crack a single password.

Appropriate fix would be to hash user passwords with Werkzeug library.  
Uncomment the fix:
https://github.com/lamtonylam/cybersecurity-project-1/blob/0692eb82a3ab90095f6c653a7d07812f38fc0096/db.py#L65

## Vulnerability 4.

### A2:2017-Broken Authentication

Not checking registering users passwords against a list of most commonly used ie. unsafe passwords, it is vulnerable for malicious actors to brute force user's accounts by guessing passwords that are commonly used, like 12345678 or qwerty.

A robust authentication design must take in mind the occasional carelessness of internet users, who use easily guessed passwords or recycle passwords from service to service.

Appropriate fix would be to check registering password against most commonly used passwords.
Uncomment to fix:
https://github.com/lamtonylam/cybersecurity-project-1/blob/0692eb82a3ab90095f6c653a7d07812f38fc0096/app.py#L33

## Vulnerability 5.

### A10:2017-Insufficient Logging & Monitoring

By not logging critical security events that happen on the website, such as failed login attempts, successful/failed registrations, and administrative page access, attackers can perform malicious activities without being detected.

Performing proper security incident investigations becomes nearly impossible without adequate logging records of user activities and system events. The lack of monitoring capabilities significantly impacts the ability to respond to and investigate security incidents in a timely manner.

Implementing logging allows the use of external monitoring platforms such as Grafana, which has built in alerting systems.
For example, when a certain specified threshold of failed login attemps triggers, it can send a slack message to the organizations' security response team.

The fix would be to implement logging using Python's logging framework.  
Uncomment to fix:
https://github.com/lamtonylam/cybersecurity-project-1/blob/0692eb82a3ab90095f6c653a7d07812f38fc0096/app.py#L17
https://github.com/lamtonylam/cybersecurity-project-1/blob/0692eb82a3ab90095f6c653a7d07812f38fc0096/app.py#L120
