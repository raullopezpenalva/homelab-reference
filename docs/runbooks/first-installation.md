# First installation: one accepted stage at a time

Begin with the [environment worksheet](../getting-started/environment.md) and
[decisions](../decisions/README.md). Use the [detailed VM tutorial](../getting-started/virtualized.md)
for versioned inputs and commands. This staged route prevents a beginner or AI
assistant from treating the whole repository as one deployment script.

| Stage | Prepare | Acceptance before advancing |
| --- | --- | --- |
| Requirements | Goals, hardware/capacity, access, persistence and recovery | Owner chooses a minimal scope; no secret values shared |
| Hypervisor/template | New lab, trusted management, reviewed storage and Ubuntu template | Console recovery, image/template identity and capacity recorded privately |
| Private inputs | New role map, networks, IDs, bootstrap DNS and public SSH key | No borrowed operational inventory; all documentation markers replaced privately |
| Offline checks | Code/config/links, schema, mock tests and scans | Record actual results and known gaps |
| One guest | Reviewed real plan and explicit owner authorization | Observed VM identity, trusted access and correct disks |
| Baseline/storage/runtime | Single-host operations with independent recovery | Correct data UUID; expected runtime paths; repeat convergence |
| Application/data | DB initialization, then separate web/API delivery | Frontend/API/SQL path and denied exposure checked |
| Foundation/telemetry | Add only needed guests/services | DNS scope and no-recursion; fresh targets and meaningful dashboard |
| Private access | Evaluate VPN/TLS/ACL design before exposure | Allowed and denied paths, DNS/IPv6, revocation and recovery |
| Recovery | Encrypted independent backup and disposable restore | Actual restored data and measured recovery evidence |

After each stage, update your private inventory and next selected task. Keep the
public reference inventory honest about code and tests only. A failed or unknown
check stops acceptance; it does not justify removing a guard or exposing another
port. Do not continue with formatting, reboots, network changes or publication
just because a guide mentions a later step.
