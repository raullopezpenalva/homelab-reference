"""Fail closed if the expected runtime filesystem is not mounted."""
import subprocess
import sys


def accepted(expected, observed):
    return len(expected) > 10 and observed.strip() == expected


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(2)
    observed = subprocess.run(["findmnt", "--noheadings", "--mountpoint", "/srv/lab", "--output", "UUID"],
                              capture_output=True, text=True, check=False)
    if observed.returncode or not accepted(sys.argv[1], observed.stdout):
        sys.exit("Reference data filesystem is unavailable or has changed")
