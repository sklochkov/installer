#!/bin/bash

BASE="http://192.168.10.169"
STAGE2_URL="${BASE}/static/discover.py"
TARGET=/usr/local/sbin/discover.py

wget -qO "${TARGET}" "${STAGE2_URL}"

chmod +x "${TARGET}"

cat << EOF > /etc/cron.d/discover
* * * * * $TARGET check
EOF

cat << EOF > /etc/discover.conf
base = ${BASE}
EOF

exec "${TARGET}" discover

