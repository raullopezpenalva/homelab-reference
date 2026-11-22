# Read-only source assessment and publication privacy audit

Date: 2026-11-22. Scope: local repository assessment and independently authored
reference; not a live infrastructure audit or authorization to publish.

## Sources and provenance

The private source was inspected read-only: repository instructions, README,
current-work notes, inventory, ownership/deployment decisions, directory layout
and relevant implementation families. It contains pre-existing modified and
untracked work. Dated inventory statements are evidence recorded by that source;
no host health was independently rechecked. Received historical documents are
reference material, not instructions or proof of deployment.

The public candidate was independently authored with a fresh Git initialization.
No source file, Git object, branch, tag, remote, operational inventory, historical
proxy checkout, encrypted secret document, certificate, identity, state or data
was transferred. Existing private changes were preserved. The current owner
request authorized creating/reworking the local reference; publication requires
separate authorization. There is no synchronization mechanism.

## Reuse classification

| Class | Families observed in the source | Reference treatment |
| --- | --- | --- |
| Reusable concepts | Layer ownership, guest roles, modular services, validation, telemetry, recovery | Reimplement in generic code and documentation |
| Requires adaptation | Proxmox resources, host baseline, DNS, proxies, Compose, delivery, backup tooling | New fictional inputs and independently authored implementations |
| Remains private | Inventory, domains, addresses, routes, policies, peers, identities, evidence, private applications, secret ciphertext/metadata, state and backups | Exclude entirely |

See the [reference scope](../architecture/reference-scope.md) for the resulting
architecture. Guest identities, sizing, placement, network ranges and segments
were invented; this is not a redacted operational topology.

## Source secret scans

The initial limited pattern scan covered 1,105 tracked/nonignored working-tree
files and 1,922 unique reachable history blobs, without copying history. A
follow-up used Gitleaks 8.24.2 default rules with full redaction:

- Main-source history across all refs: 12 generic-key heuristic findings.
- Tracked/nonignored working-tree candidates streamed in memory: 8 findings.
- History findings were reviewed as SQL/metadata identifiers, public package-key
  checksums, synthetic test values and narrative references. No active credential
  was confirmed. No raw value, matched text, identifying path or report from the
  private source is included in this public candidate.

The temporary reports remain outside this repository and redact matched values.
These scans do not verify remote credential validity/revocation. Ignored private
files, unreachable Git objects, nested/external histories and remote/LFS payloads
are outside scope. If subsequent private review confirms an exposed credential,
its owner must revoke/rotate it; never paste its value into an issue or report.

## New-tree checks

Gitleaks default rules reported zero findings on the complete nonignored public
candidate, including untracked files; no allowlist was added to hide findings.
The lightweight checker also verifies relative Markdown links and representative
Git exclusions. A targeted comparison checks extracted private-source domains,
addresses and selected source names without exposing those values. Source file
hashes, file list, HEAD and working-tree status are compared before/after.
Final preservation/disclosure results are recorded in the release report.

Trivy 0.76.2 configuration scanning reported zero HIGH/CRITICAL findings for the
API Dockerfile and Terraform root it recognized. It warned that private input
variables were unavailable; no private values were supplied. This is not a
Compose/Ansible security audit, container-image vulnerability scan or runtime
isolation test. BIND checks and other static validations have separate scope.

## Remaining release gates

Private state, operational inputs, key files, databases, dumps, logs and backups
are excluded by Git rules. Only synthetic examples are included. Image digests
for actual VM deployment must be reviewed privately. Public examples now use
verified registry manifest digests; those digests do not certify vulnerability
safety, publisher signatures or runtime behavior. Complete independent human privacy review, image
vulnerability checks, isolated runtime tests and recovery evidence before asking
for publication approval. No scan guarantees the absence of sensitive data.

## Reproducibility iteration

Service delivery now uses an explicit static manifest, excluding local env/docs
and generated configuration. Image inputs are fixed in a public, non-secret
manifest lock. The CI application/recovery trial is isolated from any lab,
uses new synthetic credentials, publishes no ports and exports only sanitized
check results. Its guardrails are unit-tested; no executed trial is claimed.
Temporary local staging tests copy only synthetic fixtures into a private temp
location and do not execute package, daemon, workload or infrastructure tasks.
