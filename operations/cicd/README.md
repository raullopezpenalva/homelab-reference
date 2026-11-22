# CI/CD: validation examples, explicit environment ownership

GitHub Actions checks this public repository. The optional
[Jenkins pipeline](jenkins/Jenkinsfile) performs selected offline checks on a
separate `reference-validation` agent. Its [controller definition](../../services/jenkins/README.md)
belongs to services, while the operating pipeline belongs here.

Neither job has a deployment identity, Docker socket, polling trigger or automatic
promotion step. Publishing/building an artifact is a different responsibility from
changing an environment. Add no production job merely to demonstrate automation.
Read the [release/data decision](../../docs/decisions/0006-release-and-data-lifecycle.md).

The GitHub `application-trial` job is a separate hosted test environment: fresh
synthetic credentials/data, no published ports, no registry push and an isolated
encrypted backup/restore trial. It installs its test-only restic client on the
hosted runner and uploads only a sanitized result. It never targets a homelab.
Its implementation is prepared; no successful job run is claimed yet.
