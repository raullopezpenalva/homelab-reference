# Delivery: validate intent, then review a separate operation

`validate.py` accepts a local release descriptor and verifies exact bundle image
keys, immutable image references, source revision and a recovery reference. It
rejects unknown fields and has no command/plugin execution path. Its result is
explicitly metadata-valid, not deployed. It does not contact a registry or prove
artifact existence, signatures, compatibility or runtime health.

Application and data lifecycles are separate. See the
[decision](../../docs/decisions/0006-release-and-data-lifecycle.md) and
[change process](../../docs/runbooks/change-management.md). Actual promotion uses
the selected Ansible service procedure after an owner approves its concrete
scope. No unattended deployment engine or production adapter is provided.
