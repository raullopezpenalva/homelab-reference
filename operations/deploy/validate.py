#!/usr/bin/env python3
"""Offline release metadata validation. Never invokes a deployer or registry."""
import argparse
import json
import re
from pathlib import Path

ALLOWED = {"ingress": {"NGINX_IMAGE"}, "applications": {"NGINX_IMAGE", "API_IMAGE"}, "database": {"POSTGRES_IMAGE"},
           "telemetry": {"PROMETHEUS_IMAGE", "GRAFANA_IMAGE"}, "automation": {"JENKINS_IMAGE"},
           "sandbox": {"NGINX_IMAGE"}}
DIGEST = re.compile(r"[a-zA-Z0-9./:_-]+@sha256:[a-f0-9]{64}")

def validate(document):
    if set(document) != {"schema", "bundle", "images", "revision", "recovery"}:
        raise ValueError("Unexpected release fields")
    if document["schema"] != "reference.release/v1" or document["bundle"] not in ALLOWED:
        raise ValueError("Unknown schema or bundle")
    if set(document["images"]) != ALLOWED[document["bundle"]]:
        raise ValueError("Image keys do not match bundle")
    if not re.fullmatch(r"[a-f0-9]{40}", document["revision"]):
        raise ValueError("Expected a reviewed source revision")
    if not isinstance(document["recovery"], str) or len(document["recovery"]) < 12:
        raise ValueError("A recovery reference is required")
    for image in document["images"].values():
        if not isinstance(image, str) or not DIGEST.fullmatch(image):
            raise ValueError("Immutable image digest required")
        if image.endswith("0" * 64):
            raise ValueError("Synthetic zero digest is not a release")
    return {"bundle": document["bundle"], "status": "metadata-valid-not-deployed"}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("descriptor", type=Path)
    args = parser.parse_args()
    try:
        result = validate(json.loads(args.descriptor.read_text()))
    except (ValueError, TypeError, KeyError):
        parser.exit(2, "Invalid release metadata; values suppressed\n")
    print(json.dumps(result))

if __name__ == "__main__":
    main()
