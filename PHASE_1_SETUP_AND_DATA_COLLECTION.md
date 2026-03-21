# 🚀 Phase 1 — Environment Setup & Log Collection

> **Goal:** Set up the development environment on Ubuntu Linux, install all dependencies, configure log sources, and collect sample log data for training.
>
> **Duration:** Week 1–2
>
> **Latest Versions Used (as of March 2026):** Ubuntu 24.04 LTS, Python 3.14, Pandas 3.0.1, NumPy 2.4.3, Scikit-learn 1.8.1, Matplotlib 3.10.8, Seaborn 0.13.2

---

## Step 1: Set Up Ubuntu Linux Environment

### What to do
Set up an Ubuntu 24.04 LTS (Noble Numbat) environment where you'll generate and collect Linux server logs.

### How to do it

**Option A — Use Docker 🐳 (Recommended — best for Mac)**

Docker is the easiest and fastest way to get a fully working Ubuntu Linux environment on your Mac. No need for a full VM.

**1. Install Docker Desktop**

- Download from: https://www.docker.com/products/docker-desktop/
- Install and launch Docker Desktop
- Verify installation:

```bash
docker --version
# Should output: Docker version 27.x or higher

docker compose version
# Should output: Docker Compose version v2.x
```

**2. Create a `Dockerfile`** in your project root (`~/Developer/01_active/sdp/`):

```dockerfile
# Use latest Ubuntu 24.04 LTS as base
FROM ubuntu:24.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install system dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    openssh-server \
    rsyslog \
    cron \
    sudo \
    tree \
    vim \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Create virtual environment and install Python dependencies
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install -r requirements.txt

# Add venv to PATH so python3/pip use the venv by default
ENV PATH="/app/venv/bin:$PATH"

# Start rsyslog to generate auth.log and syslog
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/bin/bash"]
```

**3. Create `docker-entrypoint.sh`** (starts log services inside the container):

```bash
#!/bin/bash

# Start rsyslog to generate /var/log/auth.log and /var/log/syslog
service rsyslog start

# Start cron service
service cron start

# Start SSH service (generates auth.log entries)
service ssh start

echo "✅ Ubuntu 24.04 LTS environment ready!"
echo "📁 Project directory: /app"
echo "🐍 Python: $(python3 --version)"
echo "📋 Logs available at: /var/log/auth.log, /var/log/syslog"

# Keep the container running
exec "$@"
```

**4. Create `docker-compose.yml`** (easier to manage):

```yaml
services:
  sdp-ubuntu:
    build: .
    container_name: sdp-linux-env
    hostname: sdp-server
    volumes:
      # Mount your project directory so changes sync between host and container
      - .:/app
      # Persist collected log data
      - ./data:/app/data
    stdin_open: true    # Keep container running (interactive)
    tty: true           # Allocate a terminal
    privileged: true    # Needed for rsyslog and service management
```

**5. Build and run the container:**

```bash
cd ~/Developer/01_active/sdp

# Build the Docker image
docker compose build

# Start the container in detached mode
docker compose up -d

# Enter the running container (you're now inside Ubuntu 24.04!)
docker compose exec sdp-ubuntu bash
```

**6. Useful Docker commands:**

```bash
# Check container status
docker compose ps

# Enter the running container
docker compose exec sdp-ubuntu bash

# Stop the container
docker compose down

# Rebuild after changing Dockerfile
docker compose build --no-cache

# View container logs
docker compose logs sdp-ubuntu
```

---

**Option B — Use a Virtual Machine (Alternative)**

1. Download [VirtualBox](https://www.virtualbox.org/wiki/Downloads) or use UTM (for Mac with Apple Silicon).
2. Download Ubuntu 24.04 LTS ISO from https://releases.ubuntu.com/24.04/
3. Create a new VM:
   - RAM: 2–4 GB
   - Disk: 20 GB
   - Network: Bridged Adapter (so it gets its own IP)
4. Install Ubuntu from the ISO.

**Option C — Use a Cloud VM (AWS / DigitalOcean / Azure)**

```bash
# Example: Create a DigitalOcean droplet via CLI
doctl compute droplet create sdp-server \
  --image ubuntu-24-04-x64 \
  --size s-1vcpu-1gb \
  --region blr1
```

**Option D — Use WSL2 on Windows**

```powershell
wsl --install -d Ubuntu-24.04
```

### ✅ Verify

**If using Docker (Option A):**

```bash
# Enter the container
docker compose exec sdp-ubuntu bash

# Inside the container:
cat /etc/os-release
# Should show: Ubuntu 24.04.x LTS

python3 --version
# Should show: Python 3.x

# Check that log services are running
ls -la /var/log/auth.log /var/log/syslog
```

**If using VM / Cloud / WSL (Options B–D):**

```bash
lsb_release -a
# Should show: Ubuntu 24.04.x LTS
```

---

## Step 2: Install Python 3.14+ and Dependencies

### What to do
Install Python 3.14+ and all the required ML/data libraries.

### How to do it

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python 3.14+ and pip
sudo apt install -y python3 python3-pip python3-venv git

# Verify Python version
python3 --version
# Should output: Python 3.14.x or higher
```

Now create a virtual environment and install dependencies:

```bash
# Navigate to your project directory
cd ~/sdp   # or wherever your project lives

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

Create a `requirements.txt` file:

```txt
pandas>=3.0.1
numpy>=2.4.3
scikit-learn>=1.8.1
matplotlib>=3.10.8
seaborn>=0.13.2
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### ✅ Verify

```bash
python3 -c "import pandas, numpy, sklearn, matplotlib, seaborn; print('All libraries installed successfully!')"
```

---

## Step 3: Understand Linux Log Files

### What to do
Familiarize yourself with the key log files on a Linux server that you'll be analyzing.

### Key log files

| Log File | Location | What It Contains |
|----------|----------|-----------------|
| **auth.log** | `/var/log/auth.log` | Authentication events — SSH logins, sudo usage, failed login attempts |
| **syslog** | `/var/log/syslog` | General system events — services starting/stopping, kernel messages |
| **kern.log** | `/var/log/kern.log` | Kernel-level messages |
| **nginx access.log** | `/var/log/nginx/access.log` | Web server access logs (optional) |

### How to explore them

```bash
# View recent auth.log entries
sudo tail -50 /var/log/auth.log

# View syslog entries
sudo tail -50 /var/log/syslog

# Count total lines in auth.log
sudo wc -l /var/log/auth.log

# Search for failed SSH login attempts
sudo grep "Failed password" /var/log/auth.log

# Search for successful SSH logins
sudo grep "Accepted password" /var/log/auth.log

# Search for sudo usage
sudo grep "sudo:" /var/log/auth.log
```

### Example log entries

**auth.log — Failed SSH login:**
```
Mar 21 08:30:15 server sshd[12345]: Failed password for invalid user admin from 192.168.1.100 port 54321 ssh2
```

**auth.log — Successful SSH login:**
```
Mar 21 08:31:00 server sshd[12346]: Accepted password for rahul from 192.168.1.50 port 22 ssh2
```

**syslog — Service started:**
```
Mar 21 08:32:00 server systemd[1]: Started Apache HTTP Server.
```

---

## Step 4: Set Up Project Directory Structure

### What to do
Create the folder structure for the project.

### How to do it

```bash
cd ~/sdp

# Create the directory structure
mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/sample
mkdir -p src/models
mkdir -p notebooks
mkdir -p results/figures
mkdir -p results/reports

# Create placeholder files
touch src/__init__.py
touch src/models/__init__.py
touch src/log_collector.py
touch src/log_parser.py
touch src/feature_extractor.py
touch src/models/isolation_forest.py
touch src/models/pca_detector.py
touch src/models/decision_tree.py
touch src/models/baseline.py
touch src/evaluator.py
touch src/visualizer.py
```

### ✅ Verify

```bash
tree ~/sdp -I 'venv|__pycache__'
# Should show the full project tree
```

---

## Step 5: Collect Log Data

### What to do
Copy real log files from the Linux server into your `data/raw/` directory for analysis.

### How to do it

**Method A — Direct copy (if working on the same machine)**

```bash
# Copy auth.log
sudo cp /var/log/auth.log ~/sdp/data/raw/auth.log

# Copy syslog
sudo cp /var/log/syslog ~/sdp/data/raw/syslog.log

# Make them readable
chmod 644 ~/sdp/data/raw/*.log
```

**Method B — Using SCP (if logs are on a remote server)**

```bash
# Copy from remote server to local machine
scp user@server-ip:/var/log/auth.log ~/sdp/data/raw/auth.log
scp user@server-ip:/var/log/syslog ~/sdp/data/raw/syslog.log
```

**Method C — Generate synthetic logs for testing**

Create a script `src/generate_sample_logs.py`:

```python
"""
Generate sample auth.log entries for testing.
Includes both normal and abnormal (attack) patterns.
"""

import random
from datetime import datetime, timedelta

def generate_sample_auth_log(output_file, num_entries=1000):
    normal_users = ["rahul", "ravi", "manohar"]
    attack_users = ["admin", "root", "test", "guest", "user"]
    normal_ips = ["192.168.1.50", "192.168.1.51", "192.168.1.52"]
    attack_ips = ["10.0.0.100", "10.0.0.101", "172.16.0.200"]

    base_time = datetime(2026, 3, 1, 0, 0, 0)
    entries = []

    for i in range(num_entries):
        timestamp = base_time + timedelta(seconds=random.randint(0, 86400 * 7))
        ts_str = timestamp.strftime("%b %d %H:%M:%S")

        # 70% normal, 30% abnormal
        if random.random() < 0.7:
            # Normal behavior
            user = random.choice(normal_users)
            ip = random.choice(normal_ips)
            port = random.randint(40000, 65535)

            event_type = random.choice(["accepted", "sudo", "session"])
            if event_type == "accepted":
                line = f"{ts_str} server sshd[{random.randint(1000,9999)}]: Accepted password for {user} from {ip} port {port} ssh2"
            elif event_type == "sudo":
                line = f"{ts_str} server sudo: {user} : TTY=pts/0 ; PWD=/home/{user} ; USER=root ; COMMAND=/bin/ls"
            else:
                line = f"{ts_str} server sshd[{random.randint(1000,9999)}]: pam_unix(sshd:session): session opened for user {user}"
        else:
            # Abnormal / attack behavior
            user = random.choice(attack_users)
            ip = random.choice(attack_ips)
            port = random.randint(40000, 65535)

            event_type = random.choice(["failed", "invalid", "breakin"])
            if event_type == "failed":
                line = f"{ts_str} server sshd[{random.randint(1000,9999)}]: Failed password for {user} from {ip} port {port} ssh2"
            elif event_type == "invalid":
                line = f"{ts_str} server sshd[{random.randint(1000,9999)}]: Failed password for invalid user {user} from {ip} port {port} ssh2"
            else:
                line = f"{ts_str} server sshd[{random.randint(1000,9999)}]: POSSIBLE BREAK-IN ATTEMPT from {ip}"

        entries.append((timestamp, line))

    # Sort by timestamp
    entries.sort(key=lambda x: x[0])

    with open(output_file, "w") as f:
        for _, line in entries:
            f.write(line + "\n")

    print(f"Generated {num_entries} log entries → {output_file}")


if __name__ == "__main__":
    generate_sample_auth_log("data/raw/sample_auth.log", num_entries=2000)
    print("Done! Sample log file created.")
```

Run it:

```bash
cd ~/sdp
python3 src/generate_sample_logs.py
```

### ✅ Verify

```bash
# Check the files exist
ls -la data/raw/

# Preview the log data
head -20 data/raw/sample_auth.log

# Count entries
wc -l data/raw/sample_auth.log
```

---

## Step 6: Set Up Automated Log Collection (Cron)

### What to do
Set up a Cron job that automatically copies fresh log data at regular intervals.

### How to do it

Create a collection script `src/log_collector.py`:

```python
"""
Automated log collector.
Copies latest log entries and appends them to the raw data directory.
Run this via cron for continuous collection.
"""

import shutil
import os
from datetime import datetime

# Configuration
LOG_SOURCES = {
    "auth": "/var/log/auth.log",
    "syslog": "/var/log/syslog",
}
OUTPUT_DIR = os.path.expanduser("~/sdp/data/raw")


def collect_logs():
    """Copy current log files to the data directory with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for name, source_path in LOG_SOURCES.items():
        if os.path.exists(source_path):
            dest_path = os.path.join(OUTPUT_DIR, f"{name}_{timestamp}.log")
            shutil.copy2(source_path, dest_path)
            print(f"[{timestamp}] Collected {source_path} → {dest_path}")
        else:
            print(f"[{timestamp}] WARNING: {source_path} not found, skipping.")


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    collect_logs()
    print("Log collection complete.")
```

Set up the Cron job:

```bash
# Open crontab editor
crontab -e

# Add this line to collect logs every 6 hours:
0 */6 * * * /home/rahul/sdp/venv/bin/python3 /home/rahul/sdp/src/log_collector.py >> /home/rahul/sdp/data/collection.log 2>&1
```

### ✅ Verify

```bash
# List active cron jobs
crontab -l

# Run the collector manually to test
python3 src/log_collector.py

# Check that files were created
ls -la data/raw/
```

---

## 📋 Phase 1 Checklist

- [ ] Docker Desktop installed and running
- [ ] Dockerfile and docker-compose.yml created
- [ ] Ubuntu 24.04 LTS container built and running
- [ ] Python 3.14+ available inside the container
- [ ] Virtual environment created with all dependencies (Pandas 3.0.1, NumPy 2.4.3, Scikit-learn 1.8.1, Matplotlib 3.10.8, Seaborn 0.13.2)
- [ ] Understood key Linux log files (auth.log, syslog)
- [ ] Project directory structure created
- [ ] Raw log files collected (real or sample-generated)
- [ ] Log collector script working
- [ ] Cron job configured for automated collection

---

**➡️ Next: [Phase 2 — Log Parsing & Feature Engineering](./PHASE_2_PARSING_AND_FEATURES.md)**
