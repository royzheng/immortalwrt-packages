#!/usr/bin/env python3
"""Exercise the installed hotplug route translation without touching networking."""
import os, subprocess, tempfile
from pathlib import Path
source = Path(__file__).resolve().parents[1] / 'files/usr/libexec/openvpn-hotplug'
script = source.read_text().replace('. /lib/functions.sh', '').replace('. /lib/netifd/netifd-proto.sh', '')
script = script.replace('exec /sbin/hotplug-call openvpn "$@"', ':')
stubs = '''
uci_get() { :; }
proto_init_update() { echo "link $*"; }
proto_add_ipv4_address() { echo "address4 $*"; }
proto_add_ipv6_address() { echo "address6 $*"; }
proto_add_ipv4_route() { echo "route4 $*"; }
proto_add_ipv6_route() { echo "route6 $*"; }
proto_add_host_dependency() { echo "dependency $*"; }
proto_add_dns_server() { echo "dns $*"; }
proto_add_dns_search() { echo "search $*"; }
proto_send_update() { echo "update $*"; }
json_add_int() { :; }
'''
base = dict(PATH=os.environ['PATH'], script_type='up', INTERFACE='testvpn', dev='tun0', IPV6='1',
            ifconfig_local='10.8.0.2', ifconfig_remote='10.8.0.1', route_vpn_gateway='10.8.0.1',
            ifconfig_ipv6_local='fd00::2/64', ifconfig_ipv6_remote='fd00::1', trusted_ip='192.0.2.1')
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / 'hotplug.sh'; path.write_text(stubs + script)
    def run(**extra):
        return subprocess.check_output(['/bin/sh', str(path)], env={**base, **extra}, text=True).splitlines()
    split = run(route_network_1='192.0.2.0', route_netmask_1='255.255.255.0', route_gateway_1='10.8.0.1',
                route_metric_1='7', route_ipv6_network_1='2001:db8::/32', route_ipv6_gateway_1='fd00::1',
                route_ipv6_metric_1='9', foreign_option_1='dhcp-option DNS 10.8.0.1')
    assert 'route4 192.0.2.0 24 10.8.0.1  7' in split, split
    assert 'route6 2001:db8:: 32 fd00::1 9' in split, split
    assert not any(line.startswith(('route4 0.0.0.0 ', 'route6 :: ')) for line in split), split
    assert 'address4 10.8.0.2 255.255.255.255  10.8.0.1' in split, split
    assert 'dependency testvpn 192.0.2.1' in split and 'dns 10.8.0.1' in split, split
    full = run(route_redirect_gateway='1')
    assert 'route4 0.0.0.0 0 10.8.0.1' in full, full
    halves = run(route_redirect_gateway='1', route_redirect_def1='1')
    assert 'route4 0.0.0.0 1 10.8.0.1' in halves and 'route4 128.0.0.0 1 10.8.0.1' in halves, halves
    assert 'route4 0.0.0.0 0 10.8.0.1' not in halves, halves
    down = run(script_type='down')
    assert down == ['link tun0 0', 'update testvpn'], down
print('PASS: split routes, explicit default/def1, IPv6, point-to-point, metrics, DNS and teardown')
