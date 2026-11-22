#!/bin/sh
# Run on the selected workload VM or through a separately reviewed local tunnel.
set -eu
base="http://127.0.0.1:${HTTP_PORT:-8080}"
curl --fail --silent "$base/healthz" | grep -qx ok
curl --fail --silent "$base/" | grep -q '<h1>Reference application</h1>'
curl --fail --silent "$base/api/message" | python3 -c 'import json,sys; assert json.load(sys.stdin)["message"] == "Hello from the reference database"'
echo 'Proxy, API and PostgreSQL read path passed'
