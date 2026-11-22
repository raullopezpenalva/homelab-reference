#!/usr/bin/env python3
"""Render a synthetic or private catalog without touching Terraform or the network."""
import argparse
import ipaddress
import json
import re
from pathlib import Path

ROLES = {"foundation", "applications", "telemetry", "automation", "sandbox"}

def render(config, enabled):
    if not set(enabled) <= ROLES:
        raise ValueError("Unknown role")
    names, ids, addresses = set(), set(), set()
    children = {}
    for role, guest in config["guests"].items():
        if role not in ROLES or not re.fullmatch(r"[a-z][a-z0-9-]{0,30}", guest["name"]):
            raise ValueError("Invalid role or hostname")
        address = str(ipaddress.ip_interface(guest["address"]).ip)
        if guest["name"] in names or guest["vm_id"] in ids or address in addresses:
            raise ValueError("Duplicate guest identity")
        names.add(guest["name"]); ids.add(guest["vm_id"]); addresses.add(address)
        if role in enabled:
            children[role] = {"hosts": {guest["name"]: {"ansible_host": address, "lab_role": role}}}
    if set(enabled) - set(config["guests"]):
        raise ValueError("Missing selected guest")
    return {"all": {"vars": {"ansible_user": config["bootstrap_user"], "lab_domain": config["domain"]}, "children": children}}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path(__file__).resolve().parents[2]/"infrastructure/proxmox/examples/lab.json")
    parser.add_argument("--roles", nargs="*", default=[])
    args = parser.parse_args()
    try:
        result = render(json.loads(args.config.read_text()), args.roles)
    except (ValueError, KeyError, TypeError):
        parser.error("Invalid catalog; values suppressed")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
