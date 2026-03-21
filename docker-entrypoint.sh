#!/bin/bash

# Start rsyslog to generate /var/log/auth.log and /var/log/syslog
service rsyslog start

# Start cron service
service cron start

# Start SSH service (generates auth.log entries)
mkdir -p /run/sshd
service ssh start 2>/dev/null || /usr/sbin/sshd 2>/dev/null || true

echo "✅ Ubuntu 24.04 LTS environment ready!"
echo "📁 Project directory: /app"
echo "🐍 Python: $(python3 --version)"
echo "📋 Logs available at: /var/log/auth.log, /var/log/syslog"

# Keep the container running
exec "$@"
