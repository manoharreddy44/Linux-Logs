"""
Generate sample auth.log entries for testing.
Includes both normal and abnormal (attack) patterns.

Usage:
    python3 src/generate_sample_logs.py
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
