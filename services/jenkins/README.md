# Optional Jenkins controller

The automation bundle runs a private persistent controller with zero controller executors and preserves initial setup/authentication. Configure a separate validation agent explicitly. The pipeline source lives under operations/cicd; no Docker socket or deployment credential is mounted here.

Read the [service index](../README.md), [VM guide](../../docs/getting-started/virtualized.md)
and [operating runbook](../../docs/runbooks/runbook.md) before a change.
Public image examples are fixed by digest in the validation image lock. The
operator must still review vulnerabilities and select their own API artifact. Secret contents stay outside Git and
consumer UID/permissions must be verified. No runtime acceptance is implied.
