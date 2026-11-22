# Private ingress

The logical bundle ingress belongs to a foundation guest. It demonstrates Host-based HTTP routing to explicitly selected private upstreams. Defaults use loopback; no TLS issuance, public NAT, authentication or router policy is installed.

Read the [service index](../README.md), [VM guide](../../docs/getting-started/virtualized.md)
and [operating runbook](../../docs/runbooks/runbook.md) before a change.
Public image examples are fixed by digest in the validation image lock. The
operator must still review vulnerabilities and select their own API artifact. Secret contents stay outside Git and
consumer UID/permissions must be verified. No runtime acceptance is implied.
