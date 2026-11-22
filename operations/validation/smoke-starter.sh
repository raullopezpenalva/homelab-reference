#!/bin/sh
set -eu
base="http://127.0.0.1:${HTTP_PORT:-8080}"
attempt=0
until curl --fail --silent "$base/healthz" | grep -qx ok &&
      curl --fail --silent "$base/" | grep -q '<h1>Homelab Reference</h1>'; do
    attempt=$((attempt + 1))
    if [ "$attempt" -ge 30 ]; then
        echo "Proxy/application smoke check failed" >&2
        exit 1
    fi
    sleep 1
done
echo "Proxy and application smoke checks passed"
