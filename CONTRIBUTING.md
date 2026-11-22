# Contributing

Discuss scope before adding services. Use synthetic fixtures and English docs.
Keep modules optional and configurable; document resources, boundaries, recovery
and actual validation. Run the offline checker and Compose config. Runtime tests
need a disposable, explicitly selected environment. Never include real inventory,
credentials, private reports or data. CI validates only; publishing and deployment
require separate owner authorization. Version releases using SemVer while noting
that the pre-1.0 interface may change. See [AGENTS.md](AGENTS.md).

Run `python3 operations/validation/run.py` for the basic source checks, or `--full`
with the documented tools already installed. Skipped Ansible regressions must not
be reported as complete validation. Local staging tests use a temporary directory;
they do not install packages or touch a managed host. The separate CI application
trial uses synthetic data on a fresh hosted runner and never promotes an image.
