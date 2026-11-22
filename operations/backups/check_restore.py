"""Reject restore manifests that can select an existing/reference data volume."""
import json
import sys


def validate(config):
    if config.get("name") != "reference-restore" or set(config.get("services", {})) != {"database"}:
        raise ValueError("Unexpected restore project")
    service = config["services"]["database"]
    if any(service.get(key) for key in ["container_name", "ports", "network_mode", "privileged"]):
        raise ValueError("Unexpected restore service exposure or identity")
    mounts = service.get("volumes", [])
    if len(mounts) != 1 or mounts[0].get("type") != "volume" or mounts[0].get("source") != "database":
        raise ValueError("Only the isolated database volume may be mounted")
    volumes = config.get("volumes", {})
    if set(volumes) != {"database"} or volumes["database"].get("external") or volumes["database"].get("name") != "reference-restore_database":
        raise ValueError("Restore must use its distinct project volume")
    network = config.get("networks", {}).get("app_data", {})
    if network.get("external") or network.get("name") != "reference-restore-data" or not network.get("internal"):
        raise ValueError("Restore must use its isolated private network")


if __name__ == "__main__":
    try:
        validate(json.load(sys.stdin))
    except (ValueError, KeyError, TypeError):
        sys.exit("Restore configuration rejected; details suppressed")
