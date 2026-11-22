# Security policy

This initial public preview has no supported production release. Do not use it
as an Internet security baseline. Review dependency vulnerabilities, network
policy and runtime acceptance before applying it to your own environment.

## Report a vulnerability privately

Use [GitHub private vulnerability reporting](https://github.com/raullopezpenalva/homelab-reference/security/advisories/new).
Do not open a public issue containing credentials, real infrastructure details
or exploit material that would expose another operator. Describe the affected
reference version, scope and a synthetic reproduction; never attach actual keys,
private inventories, real peers, state files or application data.

If a credential is discovered, stop sharing, notify its owner privately and
rotate/revoke it. Deleting the file does not remove prior exposure. Never paste
secret values into logs, reports, issues or agent output. Keep state, private
keys, real inventory, local configuration and backups outside Git.
