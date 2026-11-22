# Network operations: fictional templates only

`wireguard/wg0.conf.example` has invalid key markers and fictional addresses.
Do not import it into a client or router. Read the
[WireGuard rationale](../../docs/decisions/0003-wireguard-private-access.md),
[conceptual guide](../../docs/network/wireguard.md) and
[network design](../../docs/network/design.md) before adapting anything.

No actual router export, firewall rule set, VPN identity, peer map, public endpoint
or DNS inventory is included. Keep real configurations outside the public tree.
Routing, resolver behavior, IPv6 and allowed/denied flows need separate design
and runtime checks in your new lab. No script here changes a router or DNS server.
