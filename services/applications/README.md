# Application delivery

NGINX serves the frontend and routes to the example read-only API. The API joins the existing database network; this bundle does not start, migrate, restore or delete the database. Its logical bundle and guest role are both applications.

Read the [service index](../README.md), [VM guide](../../docs/getting-started/virtualized.md)
and [operating runbook](../../docs/runbooks/runbook.md) before a change.
Public image examples are fixed by digest in the validation image lock. The
operator must still review vulnerabilities and select their own API artifact. Secret contents stay outside Git and
consumer UID/permissions must be verified. No runtime acceptance is implied.
