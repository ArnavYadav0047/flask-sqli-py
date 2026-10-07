# Flask SQL Injection Demonstration Lab

> **For authorised educational and research use only.**  
> This project is a deliberately vulnerable Flask application designed to demonstrate SQL injection in a controlled lab environment. Do not deploy the insecure endpoint on a public network or use testing techniques against systems without explicit permission.

## Overview

This project demonstrates the difference between:

- An **insecure login** route that constructs an SQL query using untrusted user input.
- A **secure login** route that uses parameterized SQL queries.

The application is intended for use in a local network lab, for example:

- Raspberry Pi running the Flask application as a small IoT gateway/web service.
- Kali Linux VM acting as a controlled test client.
- macOS/Linux workstation used for development, monitoring, or packet capture.
- Wireshark used to inspect HTTP-over-TCP traffic generated during the demonstration.

The project can support a research illustration related to the **CICIoT2023** web-attack / SQL-injection category, but it does not reproduce or replace the original dataset.

## Features

- Flask-based web application.
- SQLite database with a sample user account.
- `/login_insecure` endpoint intentionally vulnerable to SQL injection.
- `/login_secure` endpoint protected with parameterized queries.
- Clear visual comparison between vulnerable and secure behavior.
- Suitable for deployment on a Raspberry Pi within a private lab network.
- Compatible with Wireshark/tcpdump traffic capture for research documentation.

## Project structure

```text
flask-sqli-lab/
├── app.py
├── init_db.py
├── database.db                 # Created locally after initialization
├── README.md
├── .gitignore
└── templates/
    ├── base.html
    ├── index.html
    ├── login_insecure.html
    └── login_secure.html
```

## Requirements

- Python 3.10 or later.
- `pip`.
- Flask.
- Git (optional, for cloning and updates).
- Raspberry Pi OS / Debian-based Linux if deploying to a Raspberry Pi.
- A private, isolated network for demonstrations.

Optional tools:

- Kali Linux VM for the controlled client/test machine.
- Wireshark or tcpdump for packet capture and traffic analysis.

## Installation

### 1. Clone the repository

```bash
git clone [https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git](https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git)
cd YOUR-REPOSITORY
```

Replace `YOUR-USERNAME` and `YOUR-REPOSITORY` with your GitHub account and repository name.

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install flask
```

### 4. Initialize the database

```bash
python3 init_db.py
```

This creates `database.db` and inserts a local demonstration account:

```text
Username: alice
Password: password123
```

## Running the application

Start the Flask development server:

```bash
python3 app.py
```

The server is configured to listen on all local network interfaces:

```python
app.run(host="0.0.0.0", port=5001, debug=True)
```

Open the application locally:

```text
http://127.0.0.1:5001/
```

From another device on the same authorised lab network:

```text
http://<SERVER-IP>:5001/
```

For example:

```text
http://192.168.1.50:5001/
```

## Application routes

| Route | Purpose |
|---|---|
| `/` | Landing page with links to both demonstrations |
| `/login_insecure` | Intentionally vulnerable login demonstration |
| `/login_secure` | Parameterized-query login demonstration |

## Demonstration workflow

Use this workflow only in your own isolated lab.

1. Open `/login_insecure`.
2. Demonstrate normal authentication using the sample account:
   - Username: `alice`
   - Password: `password123`
3. Demonstrate how insecure SQL query construction can cause an authentication bypass in the deliberately vulnerable route.
4. Open `/login_secure`.
5. Repeat the same untrusted input and show that authentication fails because the secure route uses parameterized queries.
6. Inspect the Flask terminal output to compare the insecure SQL string with the parameterized SQL query.
7. Optionally capture HTTP traffic using Wireshark for research documentation.

## Security concept

### Insecure pattern

The vulnerable route directly inserts user-controlled form data into the SQL string:

```python
query = f"""
SELECT * FROM users
WHERE username = '{username}' AND password = '{password}'
"""
```

This is unsafe because user input can alter the intended SQL syntax or logic.

### Secure pattern

The secure route separates the SQL statement from the supplied values:

```python
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cur.execute(query, (username, password))
```

Parameterized queries ensure that submitted input is treated as data rather than executable SQL syntax.

## Raspberry Pi deployment

On the Raspberry Pi:

```bash
sudo apt update
sudo apt install -y git python3-venv python3-pip
git clone [https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git](https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git)
cd YOUR-REPOSITORY

python3 -m venv venv
source venv/bin/activate
pip install flask

python3 init_db.py
python3 app.py
```

Find the Raspberry Pi IP address:

```bash
hostname -I
```

Then open the site from a Mac or Kali VM on the same private network:

```text
http://<PI-IP>:5001/
```

## Packet capture example

To capture only traffic sent to the Flask application port:

```bash
sudo tcpdump -i <INTERFACE> tcp port 5001 -w flask-sqli-lab.pcap
```

Replace `<INTERFACE>` with the interface that carries your test traffic, such as:

```text
en0
eth0
wlan0
vmnet0
```

For virtual-machine labs, traffic may use a VM interface such as `vmnet0` rather than the Wi-Fi interface.

Open the resulting `.pcap`/`.pcapng` file in Wireshark and use this display filter:

```text
tcp.port == 5001
```

You can then select a request and choose:

```text
Follow → TCP Stream
```

to inspect the HTTP request/response flow.

## Important safety notice

This repository intentionally contains insecure code for instructional purposes.

Do not:

- Deploy the insecure application to the public internet.
- Use the insecure endpoint in production.
- Test SQL injection against websites, APIs, devices, or networks you do not own.
- Store real credentials, personal data, or sensitive information in the demonstration database.

Only run the project on systems and networks where you have clear permission.

## Suggested research evidence

For a professional demonstration or report, collect:

- Screenshot of the landing page.
- Screenshot of normal login behavior.
- Screenshot showing the vulnerable route accepts unauthorised input.
- Screenshot showing the secure route rejects the same input.
- Flask terminal screenshot comparing insecure and parameterized queries.
- Wireshark screenshot showing the HTTP request flow.
- Network topology diagram: Kali VM/Mac → Raspberry Pi → Flask application and SQLite database.

## License

This project is intended for academic, educational, and authorised security-testing use. Add a license file appropriate to your institution or project requirements.
