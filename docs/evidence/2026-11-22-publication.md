# Initial public preview: hosted CI acceptance

Date: 2026-11-22. The owner explicitly authorized public repository creation and
publication of the existing MIT-licensed reference. No private source history,
remote, credentials or infrastructure configuration was transferred.

## Observed hosted result

[Workflow run 45020736851](https://github.com/raullopezpenalva/homelab-reference/actions/runs/45020736851)
completed successfully for source commit `8da908def3182ec9ae7d2001e595ae0f09ef4bda`.
All four jobs passed: static checks, Terraform mocks, secret/configuration scanning
and the isolated application/recovery trial. The
[sanitized trial artifact](2026-11-22-hosted-application-trial.json) was downloaded
and checked against the image lock; every recorded check, including cleanup,
passed. No raw runner, Docker, SQL or backup logs are published here.

The trial verified frontend/API/SQL access, denial of application writes, a
separate database identity through an application repeat, encrypted restic backup,
guarded restore into an independent empty destination and recovered data. It
published no host ports and used only new synthetic credentials/data on a hosted
runner. No image was published and no homelab host or network was contacted.

## Scope remaining open

This establishes container/application and local encrypted-recovery mechanics.
It does not establish Proxmox/template compatibility, guest package convergence,
router/VPN/TLS policy, off-host backup durability or complete disaster recovery.
Those remain separate, explicitly approved trial gates. The reference is an
initial public preview rather than a supported production deployment.

The original source repository remains unchanged. Git history for this reference
is independent, and the public repository's secret-reporting channel uses GitHub
private vulnerability reporting. Later documentation-only commits can have their
own workflow runs; the linked source run records the first accepted implementation.
