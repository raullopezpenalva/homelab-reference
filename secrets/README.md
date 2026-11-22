# Secrets: policy and custody references only

This public category intentionally contains only this README. It mirrors the
responsibility of secret management without mirroring anyone's real secret store.
All other contents under `secrets/` are ignored by default. Do not place real
material here even temporarily; ignored is not an encryption or access control.

Keep credentials, private keys/certificates, actual WireGuard peers, real
inventories, Terraform states/plans, local environment files, DB dumps and backups
in a protected store outside this public workspace. Keep actual SOPS ciphertext
and recipient/identity metadata in a separate private store too. No decryption
identity, secret creation rule with real recipients or master credential is given
to CI, a VM or an AI environment by copying this repository.

Learn the [reasoning](../docs/decisions/0005-secrets-and-custody.md) and
[lifecycle](../docs/security/secrets.md), then decide your own custody and recovery.
Use existing `.env.example` files and private-input examples as field guides;
replace their placeholders privately, never in a public commit.

A backup of a credential without its recovery identity may be unusable. A master
identity copied to every consumer creates unnecessary authority. Deliver only
the needed file and verify the consumer's UID/permissions. Test key recovery,
consumer rotation and lost-device revocation with synthetic material first.
