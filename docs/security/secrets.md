# Secret handling through the lab lifecycle

[The custody decision](../decisions/0005-secrets-and-custody.md) explains why.
[The secrets category](../../secrets/README.md) defines what can be public.

| Stage | Professional practice | Public reference boundary |
| --- | --- | --- |
| Design | List consumers, privileges, lifetime and recovery owner | Role descriptions only; no actual identities |
| Create | Use a private prompt/tool and protected files | No pasted value or generated identity here |
| Store | Human manager and reviewed encrypted private store | No actual plaintext or ciphertext/recipient metadata |
| Deliver | Only the selected consumer's file, with verified UID/permissions | Paths/examples only; no master key in a VM or CI |
| Operate | Scope access and avoid credential-bearing logs/arguments | No live endpoints, credentials or exported logs |
| Rotate | Update stored value and consumer atomically enough for recovery | Changing a file alone does not rotate a DB role |
| Recover/revoke | Independent recovery path and tested lost-device procedure | Synthetic rehearsals and redacted evidence only |

File-backed Compose secrets inherit host access constraints; verify the UID and
permissions of the selected image. Do not solve an access failure by making the
whole secret directory publicly readable. Terraform states/plans, database dumps
and application backups are sensitive artifacts even if no token scanner matches.

For an AI-assisted change, reference a private file and explain its purpose;
do not ask the assistant to print it. If a secret is exposed, stop sharing,
notify its owner privately and revoke/rotate it. Removing the current file is
insufficient if a value was already exposed or recorded in history.
