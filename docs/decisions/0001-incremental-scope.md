# ADR 0001: The virtualized infrastructure is the primary reference

Date: 2026-11-22. Status: accepted; supersedes the initial Starter-only scope.

A container-only example does not represent the infrastructure engineering this
project should teach. The reference must include Proxmox guests, Terraform,
Ansible, service-specific responsibilities, data persistence, telemetry and
recovery, while protecting the private source.

Independently implement those layers using a fictional catalog and topology.
Keep Starter as an optional introduction, not the central architecture. Use
reviewed inputs and opt-in operations. Distinguish code, static/mocked tests and
actual environment acceptance. No private file or historical Git object is
imported; no publication or deployment permission follows from authoring.

Trade-offs: the public example is less complex than a fully operated lab.
Router/VPN/TLS policy, centralized logs, tracing and IoT are extensions. Disk
formatting and bare-metal installation remain explicit operator responsibilities.
This preserves a reviewable learning path without shipping production credentials
or a network policy derived from someone's installation.
