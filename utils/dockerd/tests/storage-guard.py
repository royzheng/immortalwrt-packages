"""Filesystem/command fixtures exercise the shipped startup guard without mounting disks."""
from pathlib import Path
import tempfile, subprocess, os
source=(Path(__file__).resolve().parents[1]/'files/docker-storage-check').read_text()
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp);bin=p/'bin';bin.mkdir()
 scripts={'uci':'case "$3" in *.data_mount) echo "$TEST_MOUNT";; *.data_root) echo "$TEST_ROOT";; esac',
 'readlink':'echo "$2"','logger':':','df':'echo "Filesystem 1024-blocks Used Available Capacity Mounted"; echo "disk 1000000 100 $TEST_FREE 1% $TEST_MOUNT"'}
 for name,text in scripts.items():
  f=bin/name;f.write_text('#!/bin/sh\n'+text+'\n');f.chmod(0o755)
 (p/'guard').write_text(source.replace('/proc/mounts',str(p/'mounts')))
 cases=[('valid','/mnt/data','/mnt/data/docker','ext4','rw',400000,True),('overlay','/mnt/data','/mnt/data/docker','overlay','rw',400000,False),('readonly','/mnt/data','/mnt/data/docker','ext4','ro',400000,False),('system','/overlay','/overlay/docker','ext4','rw',400000,False),('modem','/mnt/vendor/nvdata','/mnt/vendor/nvdata/docker','ext4','rw',400000,False),('ram','/tmp/data','/tmp/data/docker','ext4','rw',400000,False),('escape','/mnt/data','/other/docker','ext4','rw',400000,False),('full','/mnt/data','/mnt/data/docker','ext4','rw',100,False),('unmounted','/mnt/data','/mnt/data/docker','ext4','rw',400000,False),('alias','/mnt/data','/mnt/data/docker','ext4','rw',400000,False)]
 for name,mount,root,fs,mode,free,ok in cases:
  (p/'mounts').write_text('' if name=='unmounted' else f'/dev/test {mount} {fs} {mode} 0 0\n'+('/dev/test /mnt/vendor/nvdata ext4 rw 0 0\n' if name=='alias' else ''))
  env=dict(os.environ,PATH=str(bin)+':'+os.environ['PATH'],TEST_MOUNT=mount,TEST_ROOT=root,TEST_FREE=str(free))
  result=subprocess.run(['sh',str(p/'guard')],env=env,capture_output=True,text=True)
  assert (result.returncode==0)==ok,(name,result.stderr)
print('PASS Docker storage cases: mounted writable disk required; system/modem/RAM/escape/full denied')
