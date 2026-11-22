# Optional Starter: one Linux host, small Compose exercise

The main learning path is the [VM reference](virtualized.md). This exercise is
self-contained under `services/starter/`; it demonstrates proxy/app separation
and optional Prometheus self-monitoring without configuring a hypervisor.

1. Use an explicitly selected disposable Docker host. Inspect `docker context show`
   and `docker context inspect`; remote engines bind ports on the remote host.
2. Run `python3 operations/validation/check.py` from the repository root, then
   change directory with `cd services/starter`.
3. Copy `.env.example` to an ignored `.env`, review images and choose available
   loopback ports. No actual credential is required by this demonstration.
4. Run `docker compose --env-file .env config --quiet`. This parses local files;
   it does not start a daemon or deploy containers.
5. Only after approving that local trial, run `docker compose up -d`. This may
   pull public images and creates the selected project/network on that engine.
6. From this directory run `sh ../../operations/validation/smoke-starter.sh`.
   If you changed the port, pass `HTTP_PORT=your_port` to that script.
7. Open <http://localhost:8080>. Optionally start monitoring with
   `docker compose --profile monitoring up -d` and inspect
   <http://localhost:9090/targets>. Its target is Prometheus itself.
8. Stop with `docker compose --profile monitoring down`. Do not add `--volumes`
   unless you explicitly intend to delete retained metrics.

No router, host DNS, firewall or VPN changes are needed. Do not forward the ports
to the Internet. Read the [operating runbook](../runbooks/runbook.md) before
updates/persistence changes. Runtime success requires your own smoke evidence;
static checks performed during authoring do not establish it.
