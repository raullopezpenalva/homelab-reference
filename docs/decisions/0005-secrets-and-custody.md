# ADR 0005: Private secret custody, public policy

Date: 2026-11-22. Status: custody design, no real key or ciphertext included.

The public reference must be safe to share with a friend and an AI environment.
Secret custody must remain usable if the usual controller, DNS or CI is down.
Choose a human password manager for interactive access and evaluate SOPS with age
for private structured IaC inputs. SOPS supports encrypted structured files;
age supplies an encryption/identity mechanism. Neither removes the need to
protect decryption identities and plaintext delivery.
[SOPS documentation](https://getsops.io/docs/) and [age documentation](https://github.com/FiloSottile/age)
describe the tools; this is not an implemented integration.

Keep actual inputs and encrypted catalogs in a separate private store/workspace.
Even encrypted files can reveal recipients, names, structure or service metadata,
so this public repository rejects them by default. `secrets/README.md` contains
only policy. Consumers receive only their required file secret, not an operator's
master identity or an entire catalog. Terraform state/plans need their own
protection; `sensitive` output flags do not encrypt a state file.

Alternatives: Ansible Vault may be sufficient for an Ansible-focused workflow;
private files can bridge an early disposable trial if permissions and destruction
are explicit; a server-based secret manager needs a justified availability and
bootstrap design. Do not build a service solely to store the credential required
to recover that same service.

Before using actual secrets, decide custody, per-service privilege, recovery,
rotation and revocation. Test recovery with synthetic material first and retain
an independent recovery path. See [secret handling](../security/secrets.md).
