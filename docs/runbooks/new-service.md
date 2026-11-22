# Introduce a new service without losing the structure

1. State a user need and why an existing service is insufficient. Evaluate the
   maintenance, exposure, resource and recovery cost before choosing software.
2. Decide source/build ownership, guest role, bundle and runtime/data lifecycle.
   Explain a meaningful new choice in `docs/decisions/`.
3. Put resource provisioning/host configuration under `infrastructure/`, service
   definitions under `services/`, operating tools under `operations/`, and reasons,
   procedures/status under `docs/`. Keep actual secret material outside the repo.
4. Define variables, immutable artifacts, private binds/networks, resource limits,
   persistent volumes, consumer UID/permissions and minimum credentials.
5. Describe startup checks, negative/denied paths, update compatibility, backup,
   restoration and retirement. Database lifecycle is a separate change.
6. Validate offline and update category indexes, the AI instructions when needed,
   reference inventory and acceptance criteria. Do not mark runtime complete.
7. Obtain approval for a small disposable trial, record actual results and amend
   the private environment inventory. Add scheduling or unattended delivery only
   for an explicitly chosen need with its own failure/recovery design.

Use [the change process](change-management.md) and
[service index](../../services/README.md). Never copy private application source,
operational inventory or historical deployment workflows as a shortcut.
