"""Exercise actual shell functions with mock ip/uci; no host routes are changed."""
from pathlib import Path
import re, subprocess
root=Path(__file__).resolve().parents[1]
lib=(root/'files/lib/mwan3/mwan3.sh').read_text()
init=(root/'files/etc/init.d/mwan3').read_text()
def function(source,name):
 return re.search(r'^'+name+r'\(\)\s*\{.*?^}',source,re.M|re.S)[0]
def run(code):return subprocess.run(['bash','-c',code],check=True,text=True,capture_output=True).stdout
for family in ('ipv4','ipv6'):
 out=run('''config_get() { export "$1=$fixture_family"; }
mwan3_get_iface_id() { export "$1=2"; }
mwan3_id2mask() { echo 0x20000; }
mock4() { echo "ipv4 $*"; }
mock6() { echo "ipv6 $*"; }
IP4=mock4; IP6=mock6; NO_IPV6=0; MMX_MASK=0x003f0000
'''+f'fixture_family={family}\n'+function(lib,'mwan3_delete_iface_rules')+'\nmwan3_delete_iface_rules modem5g')
 lines=out.splitlines();assert len(lines)==3 and all(l.startswith(family) for l in lines),out
 assert '1888' not in out and '0x20000/0x003f0000' in out and 'lookup 2' in out
# disabled start must not initialize state or rules
out=run('uci() { echo 0; }; mwan3_init() { echo UNEXPECTED; };\n'+function(init,'start_service')+'\nstart_service')
assert not out,out
# A stopped service must not remove any route rules.
out=run('MWAN3_STATUS_DIR=/path/that/does/not/exist; mwan3_init() { echo UNEXPECTED; };\n'+function(init,'stop_service')+'\nstop_service')
assert not out,out
assert (0x003f0000 & 0x162)==0 and (0x003f0000 & 0x1a0a)==0
print('PASS disabled start/stop, exact IPv4/IPv6 rule cleanup and proxy mark separation')
# A removed/reordered UCI interface still has its old installed ID; cleanup uses the journal.
import tempfile
with tempfile.TemporaryDirectory() as tmp:
 path=Path(tmp)/'owned_rules';path.mkdir();(path/'ipv4-2').write_text('ipv4 2 0x20000/0x003f0000 old-uplink\n')
 out=run(f'MWAN3_STATUS_DIR={tmp}\n'+'''IP4=mock4; IP6=mock6
mock4() { echo "ipv4 $*"; }
mock6() { echo "ipv6 $*"; }
'''+function(lib,'mwan3_delete_owned_rules')+'\nmwan3_delete_owned_rules')
 assert 'pref 1002 iif old-uplink lookup 2' in out and 'route flush table 2' in out and '1888' not in out,out
print('PASS removal/reordering cleans the recorded installed interface without a current UCI entry')
