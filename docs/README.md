# Documentation: understand, decide, implement, operate

Read in this order. You do not need to understand every tool before starting.

1. [AI handoff](getting-started/ai-handoff.md): how to use this repository with an
   assistant, what to ask and how to retain control of changes.
2. [Environment worksheet](getting-started/environment.md): gather needs and
   constraints before selecting hardware roles, networks or services.
3. [Architecture](architecture/overview.md) and [reference scope](architecture/reference-scope.md):
   understand layers, fictional examples and what is deliberately excluded.
4. [Decisions](decisions/README.md): reasons, alternatives and trade-offs.
5. [Reference inventory](inventory.md): distinguish code, templates, checks and
   actual deployment acceptance.
6. [First installation](runbooks/first-installation.md) and [detailed VM guide](getting-started/virtualized.md):
   proceed by approved stages, with a clear stopping point after each.
7. [Change management](runbooks/change-management.md), [new services](runbooks/new-service.md)
   and [operating runbook](runbooks/runbook.md): keep the lab understandable later.
8. [Security audit](security/audit.md), [secret handling](security/secrets.md) and
   [release readiness](release-readiness.md): review disclosure and test limits.

## Find a category

- architecture/: relationships and scope, not operational inventory.
- decisions/: dated reasoning, alternatives and consequences.
- getting-started/: learning path, adaptation and setup tutorials.
- network/: addressing/DNS/VPN/TLS concepts and fictional design.
- runbooks/: operator steps, acceptance and recovery.
- security/: threat/custody considerations and privacy audit.
- templates/: reusable records with no real environment values.

A design, a source declaration and a verified deployment are different facts.
For observed state, record date, scope, check and result. Keep real host details,
logs and private evidence outside this public reference.

## Portfolio and reproducibility

- [Engineering case study](portfolio/case-study.md): problem, decisions and evidence limits.
- [Reproducible trial paths](getting-started/reproducible-trial.md): local, hosted app and VM acceptance.
- [Dependency selection](runbooks/dependency-updates.md): public image baseline and private package inputs.
- [Observed iteration evidence](evidence/2026-11-22-reproducibility.md): actual results, not deployment claims.
