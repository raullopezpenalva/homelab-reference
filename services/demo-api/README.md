# Educational API source

This small read-only PostgreSQL example exists so a new owner can build an artifact and test the whole frontend/API/data path. It contains no private application logic. In an operated system, application source/build normally belongs in its own repository, while this infrastructure repo selects image digests and delivery configuration.

Read the [service index](../README.md), [VM guide](../../docs/getting-started/virtualized.md)
and [operating runbook](../../docs/runbooks/runbook.md) before a change.
Public image examples are fixed by digest in the validation image lock. The
operator must still review vulnerabilities and select their own API artifact. Secret contents stay outside Git and
consumer UID/permissions must be verified. No runtime acceptance is implied.
