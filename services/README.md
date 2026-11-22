# Services: definitions grouped by responsibility

Source directories describe responsibilities; logical Ansible bundle keys stay
stable for private operation inputs. The source mapping lives in
`infrastructure/ansible/roles/bundle/vars/main.yml`. No source directory identifies
an actual running host or implies deployment acceptance.

| Source category | Logical bundle / role | Purpose |
| --- | --- | --- |
| [applications/](applications/README.md) | applications / applications | Frontend and API delivery |
| [database/](database/README.md) | database / applications | Independent PostgreSQL lifecycle |
| [demo-api/](demo-api/README.md) | Build example, not a bundle | Educational app source only |
| [internal-proxy/](internal-proxy/README.md) | ingress / foundation | Optional private HTTP entry |
| [observability/](observability/README.md) | telemetry / telemetry | Prometheus/Grafana definitions |
| [jenkins/](jenkins/README.md) | automation / automation | Optional CI controller runtime |
| [sandbox/](sandbox/README.md) | sandbox / sandbox | Optional private development demo |
| [starter/](starter/README.md) | Standalone profile | Small optional Compose learning exercise |

Native authoritative DNS is configured by the Ansible DNS role, not a second
competing Compose implementation. Read [the architecture](../docs/architecture/overview.md)
and [new-service procedure](../docs/runbooks/new-service.md). Actual image digests,
secret files, binds, storage UUIDs and inventory belong in private inputs.
