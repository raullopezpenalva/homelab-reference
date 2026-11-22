# ADR 0003: WireGuard for scoped private administration

Date: 2026-11-22. Status: reference design; template only, no tunnel deployed.

## Problem and choice

An operator needs a private path to selected administration services without
publishing each management UI to the Internet. For a small lab with a manageable
number of devices, choose WireGuard as the example VPN: peers are identified by
public keys and carry traffic through an encrypted tunnel. Its peer/address model
is small enough to explain alongside routing. This is a design choice, not a
performance claim or a guarantee of correct access control.
[WireGuard's conceptual overview](https://www.wireguard.com/) explains this model.

## Alternatives and trade-offs

| Option | Useful when | Cost or limit |
| --- | --- | --- |
| SSH tunnel | One operator needs one temporary service | Multiple client/service paths can become manual |
| WireGuard | A few devices need a defined private network path | You operate peer lifecycle, endpoint reachability, routes and DNS |
| OpenVPN or IPsec | Existing organizational tooling or interoperability decides the choice | Requires its own configuration and operational expertise |
| Managed/mesh VPN | Enrollment or difficult connectivity is the main constraint | Evaluate control-plane trust, dependencies and recovery separately |

WireGuard is not an application authorization service or a complete firewall.
A key identifies a peer; it does not establish a human role or require every
application to permit access. One device should not receive all lab routes just
because it needs one UI. Administrative and ordinary application access should
be designed separately.

## Consequences and acceptance

Create new keys privately per device. Define which destinations each client
needs, how DNS resolves them, and how server/client/firewall policy enforces that
scope. Decide how to revoke a lost device and recover the server without relying
on that same tunnel. Never publish real peer files or key metadata.

The [network guide](../network/wireguard.md) explains the pieces and a test order.
The [teaching template](../../operations/network/wireguard/wg0.conf.example)
contains invalid key markers and fictional addresses. It cannot establish
reachability, peer isolation, IPv6 behavior, DNS correctness or device revocation;
those require an explicitly authorized lab trial.
