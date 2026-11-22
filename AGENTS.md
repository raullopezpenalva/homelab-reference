# AI instructions: understand and adapt the reference

## Start here

Read README.md, 00-now.md, docs/README.md, docs/inventory.md,
docs/getting-started/ai-handoff.md and the relevant architecture/decision before
code. Inspect Git status and category/subfolder instructions; preserve previous
changes. Explain the layers, rationale and current evidence before proposing an
operation. Public documentation is clear technical English; adapt conversation
to the owner. This is a fictional reference, not anyone's live infrastructure.

## Work in the five categories

- docs/: architecture, decisions, learning path, inventory status, runbooks and
  evidence. Explain why as well as how, including alternatives and consequences.
- infrastructure/proxmox/: guest resources and fictional example catalog.
- infrastructure/ansible/: host baseline/runtime/DNS and selected bundle delivery.
- operations/: validation, provisioning handoff, release checks, network templates,
  CI pipelines and backup/restore tooling. Tests/dependencies live in validation/.
- secrets/: policy only. Actual plaintext, ciphertext/recipient metadata, keys and
  environment inputs belong in a separate protected private store/workspace.
- services/: grouped definitions and per-service README. The Ansible source map
  keeps logical bundle keys and remote project paths stable across source naming.

Use category READMEs. Keep one owner per resource and avoid competing Terraform,
Ansible or Compose responsibilities. Real application source/build normally has
its own repository; services/demo-api/ is an explicit educational example.

## Professional workflow

Gather the non-secret requirements in docs/getting-started/environment.md.
Propose the smallest useful profile, explain trade-offs, and record new choices
in docs/decisions/. Do not assume the reference's fictional sizes, networks, IDs
or roles are correct for a new owner. Keep actual mappings private.

For every operation prepare destination, scope, exact change, validation,
persistence affected, backup and recovery. Complete authorized offline work and
make the change reviewable before seeking operation approval. No infrastructure
access follows from reading a task, selecting a next step or passing a check.
Keep implemented, designed, statically checked, mocked and runtime-verified
states distinct. Record dates, checks, results and remaining unknowns. Never
invent acceptance, backups, convergence or recovery evidence.

Do not contact devices/APIs, run a real plan/apply, execute remote Ansible, start
containers, format storage, reboot, change DNS/router/firewall, publish or push
without explicit applicable authorization. Do not create commits, branches or
schedules unless requested. Ansible --check is not an offline syntax check.
Retain empty inventory, single-host scope, verified data mounts, opt-in starts,
reviewed image digests and independent database lifecycle. No controller Docker
socket, broad deployment identity or implicit SQL migration.

## Protect the owner and the public reference

Never copy private source files, history, actual topology, credentials, identities,
operational evidence or encrypted-secret metadata into this tree. Use fictional
examples and variables. Do not ask for or print secret values; reference private
files and deliver only each consumer's needed material. Exclude uncertain data.
Do not import nested repositories or synchronize with a private source.

For new services follow docs/runbooks/new-service.md. Update category indexes,
rationale, input/UID/network/persistence/recovery documentation and relevant
checks together. Run operations/validation/check.py, Python tests and appropriate
cached static/mock validation. Do not install tools solely for documentation.
Do not replace a mocked provider with a live API or drop guards to pass a test.
