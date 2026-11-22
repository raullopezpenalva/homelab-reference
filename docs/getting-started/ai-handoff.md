# Give this repository to your AI assistant

The goal is to help you build **your** homelab with a professional process. The
repository supplies structure, working examples and reasoning; it cannot know
your hardware, network policy, credentials or recovery constraints.

## Start the conversation

Open the repository as the assistant's workspace and supply this prompt:

```text
Read AGENTS.md, README.md, 00-now.md, docs/README.md, docs/inventory.md and the
architecture/decision documents before editing. Treat this as a fictional
reference, not as my live inventory.

Help me understand the layers and gather the requirements in
docs/getting-started/environment.md. Explain technology choices and alternatives
in plain language. Ask only for decisions needed for the current stage.

Prepare an adaptation plan for my own lab. Keep actual addresses, hostnames,
keys, credentials and operational inputs outside the public tree. Do not ask me
to paste secrets into chat. Use references to private files instead.

Work in the existing categories: docs, infrastructure, operations, secrets and
services. Preserve prior changes. Before an operation, identify destination,
scope, validation, affected persistence, backup and recovery. Start with offline
checks. Do not contact devices, deploy, format, reboot, change network policy,
create commits or publish until I authorize that concrete operation.

Separate implemented code, designs, static checks, mocked tests and observed
runtime evidence. Begin by explaining the repository and listing the missing
non-secret requirements. Do not deploy yet.
```

## Work in small stages

| Stage | Assistant prepares | Owner decides | Evidence before advancing |
| --- | --- | --- | --- |
| Understand | Plain-language architecture and role map | Goals and constraints | Completed worksheet; no infrastructure access |
| Design | Minimal profile, alternatives, capacity and recovery proposal | Chosen architecture | Your own ADRs and private-input references |
| Adapt | Reviewable file changes and private-input templates | Scope of first guest | Offline checks; no copied operational values |
| Provision | Exact destination and reviewed plan/recovery procedure | One explicit operation | Observed VM identity and trusted access |
| Configure | One baseline/runtime/service change at a time | Packages, storage and exposure | Actual checks and repeat convergence |
| Accept | Health, denied-flow and restoration procedure | Whether evidence is sufficient | Dated results and remaining limitations |
| Maintain | Update proposal and recovery trigger | Whether/when to proceed | Compatible artifacts and tested recovery |

The assistant should finish authorized offline preparation before asking you to
approve an operation. Reading a guide, selecting a task or passing a lint check
is not approval to apply it. A response timeout is not consent.

## Keep knowledge useful

Use `00-now.md` for selected next work, your private inventory for observed real
state, ADRs for reasoning, and runbooks for repeatable procedures. Keep public
reference status in `docs/inventory.md` free of real environment details.
Document failures and unknowns rather than inventing evidence. Save private
results locally with the [change record](../templates/change-record.example.md).

Useful follow-up prompts:

- "Explain why WireGuard is proposed here and when an SSH tunnel is enough."
- "Adapt the guest budget to my constraints; propose the smallest first step."
- "Review the DNS bootstrap dependency without changing my resolver."
- "Prepare a one-guest change and recovery plan for review; do not execute it."
- "Explain how I would prove a backup can restore without touching my main DB."
