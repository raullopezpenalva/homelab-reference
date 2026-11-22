# Independent PostgreSQL lifecycle

This project owns its database volume and private data network. Initial role/schema setup runs only on an empty volume. The application role reads a single example table; admin and application passwords are separate external files. Its logical bundle is database and its guest role is applications.

Read the [service index](../README.md), [VM guide](../../docs/getting-started/virtualized.md)
and [operating runbook](../../docs/runbooks/runbook.md) before a change.
Public image examples are fixed by digest in the validation image lock. The
operator must still review vulnerabilities and select their own API artifact. Secret contents stay outside Git and
consumer UID/permissions must be verified. No runtime acceptance is implied.
