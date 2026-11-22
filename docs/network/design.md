# Fictional networks, DNS, VPN and TLS

These values are an independently invented teaching design. They do not describe
or reproduce any private router, topology, VLAN, firewall policy or actual peer.
No router/firewall/bridge is configured by this repository.

| Zone | Fictional range / VLAN | Intended use |
| --- | --- | --- |
| Management | 10.64.10.0/24 / 210 | Operator and hypervisor access |
| Services | 10.64.20.0/24 / 220 | DNS, telemetry and optional CI |
| Workloads | 10.64.30.0/24 / 230 | Reference application VM |
| IoT | 10.64.40.0/24 / 240 | Future isolated experiments |
| Development | 10.64.50.0/24 / 250 | Optional sandbox |
| VPN clients | 10.64.60.0/24 | Separate remote-access design |
| Public documentation | 192.0.2.0/24 | Explanatory addresses, never routable endpoints |

Terraform only assigns a guest NIC to the bridge/VLAN supplied by the operator.
It does not create bridges, trunk ports, routing, DHCP or an allow/deny policy.
Single-NIC guests avoid making an application VM an unintended router.

## Flow review worksheet

Start with isolation and choose only necessary flows. This worksheet expresses
reference intentions, not a deployable firewall or a statement of enforcement.

| Source | Destination | Proposed purpose |
| --- | --- | --- |
| Authorized operator | Proxmox HTTPS / guest SSH | Administration |
| Approved DNS clients | Foundation UDP/TCP 53 | Authoritative fictional zone |
| Private ingress | Selected backend HTTP ports | Explicit reverse proxy paths |
| Telemetry | Approved guest TCP 9100 | Host metrics only |
| API container | Database container TCP 5432 | Docker-internal read-only application access |
| Backup operator | Encrypted backup storage | Explicit backup/restore operation |
| IoT clients | Selected future broker only | No general management access |

There is no PostgreSQL host port and no Docker socket mounted into CI. Docker
port publishing and its firewall chains need separate testing; a diagram or
UFW rule does not establish container isolation. Review IPv6 independently and
test denied paths from each zone as well as intended paths. The baseline exporter
binds to the guest IP; restrict it before enabling that baseline.

## DNS

BIND9 is authoritative-only for `lab.example.com`, limited to explicit query
clients, with recursion, transfers and dynamic updates disabled. It has no real
upstream/private records. Bootstrap uses a separate operator-selected resolver.
Use conditional forwarding for the fictional zone if adding recursive resolution;
do not replace a functioning resolver with this authoritative-only server.

The Starter uses Docker service DNS and loopback ports; it does not create any
of these networks or modify host DNS. Private ingress Host headers must match
the fictional/private domain you configure.

## VPN

The [WireGuard example](../../operations/network/wireguard/wg0.conf.example) contains
invalid key markers and fictional addresses only. It is not an installation or
an actual peer configuration. Generate keys privately per device, review
AllowedIPs in both directions, choose route scopes and separately test router,
forwarding, DNS and IPv6 behavior. Never copy someone else's endpoint or peer
identity. VPN connectivity by itself does not authorize management access.

## TLS and public ingress

The executable HTTP bundles default to loopback and support a trusted tunnel
learning workflow. Shared/private-network exposure needs independently verified
ACLs; public exposure also needs TLS, authentication and an operator-reviewed
threat model. No public NAT/port-forward rule is supplied. Decide certificate
issuer, renewal identity, private key custody, serving UID, delivery, reload and
expiry monitoring before adding TLS termination. Certificates are external
material; no real CA account, domain validation credential or wildcard is bundled.
