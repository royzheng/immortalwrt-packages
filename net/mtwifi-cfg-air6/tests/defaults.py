from pathlib import Path
import subprocess, tempfile
source=(Path(__file__).resolve().parents[1]/'files/lib/wifi/air6-defaults.sh').read_text().replace('. /lib/functions.sh','')
with tempfile.TemporaryDirectory() as tmp:
 phy=Path(tmp)/'phy7';phy.mkdir()
 mock='''config_get() {
 case "$3" in
  main_ifname) eval "$1=rai";;
  band) eval "$1=5g";;
  channel) eval "$1=149";;
  htmode) eval "$1=EHT80";;
  country) eval "$1=JP";;
  disabled) eval "$1=1";;
 esac
}
uci() { case "$2" in set) echo "$3";; esac; }
'''+f'readlink() {{ echo {phy}; }}\n'
 out=subprocess.check_output(['bash','-c',source+mock+'air6_repair_radio radio1'],text=True)
 assert out.strip()=='wireless.radio1.phy=phy7',out
 missing=mock.replace('eval "$1=149"','eval "$1="').replace('eval "$1=EHT80"','eval "$1="')
 out=subprocess.check_output(['bash','-c',source+missing+'air6_repair_radio radio1'],text=True)
 assert 'channel=36' in out and 'htmode=EHT160' in out and 'country=' not in out,out
 fresh=mock.replace('eval "$1=rai"','eval "$1=rax"')
 out=subprocess.check_output(['bash','-c',source+fresh+'AIR6_WIRELESS_FRESH=1; air6_repair_radio radio2'],text=True)
 assert 'band=6g' in out and 'country=CN' in out and 'disabled=1' in out and 'htmode=EHT320' in out,out
print('PASS custom radio fields preserved, missing fields repaired, dynamic PHY and fresh CN 6GHz disabled')
