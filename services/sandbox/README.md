# Optional development sandbox

The sandbox bundle is a small private web demo on its own guest role. It contains no shared application, real dataset or route into a management network. Omit it until a concrete development use case exists.

Read the [service index](../README.md), [VM guide](../../docs/getting-started/virtualized.md)
and [operating runbook](../../docs/runbooks/runbook.md) before a change.
Public image examples are fixed by digest in the validation image lock. The
operator must still review vulnerabilities and select their own API artifact. Secret contents stay outside Git and
consumer UID/permissions must be verified. No runtime acceptance is implied.
