# Professional change process

Professional operation is a repeatable decision and evidence process, not the
number of tools or services installed. Use the
[change-record template](../templates/change-record.example.md) privately.

1. Describe the problem and current **observed** state. Mark declarations,
   historical designs and untested assumptions separately.
2. Identify the owner: VM resource, guest OS/runtime, service, database, network,
   identity or backup. Keep one authority per resource.
3. Prepare the smallest reviewable change. Record destination, scope, exact
   inputs, expected behavior and data/persistence affected. An AI can do this
   preparation without infrastructure access.
4. Define checks, failure triggers, backup reference and concrete recovery.
   Rebuild may be enough for disposable configuration; persistent data needs a
   verified restoration path. Do not invent a backup/restore result.
5. Run appropriate offline checks. Review the resulting diff and exclusions.
   Then authorize only the concrete operation you actually intend to execute.
6. Execute within that scope and collect bounded, redacted evidence. Stop for an
   unexpected destination, data change or failed check; reassess recovery.
7. Verify resulting health, isolation and persistence. Repeat configuration to
   measure convergence when appropriate. Record date/result and remaining limits.
8. Update private inventory, relevant runbook/decision and selected next work.
   Publication, pushes and scheduled automation are separate decisions.

Application release checks do not authorize SQL or a database restore. A stopped
container is not evidence of discarded data. A snapshot is not independent
recovery. Review those boundaries before choosing a rollback action.
