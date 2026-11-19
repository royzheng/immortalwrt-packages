# AIR6 wireless runtime

`mtwifi` is the existing prebuilt daemon from the maintainer bundle. It requires
`libubox.so.20260523` and `libubus.so.20260628`; the newer system SONAMEs do not
satisfy those ELF dependencies.

The matching libraries were recovered on 2026-11-17 from the previous build's
`/home/debian/immortalwrt-air6/build_dir/target-aarch64_cortex-a55+neon-vfpv4_musl/root-mediatek/usr/lib/`
on the build host. Their SONAMEs match their filenames, and this libubus requires
the bundled `libubox.so.20260523`. Install only the versioned filenames so that
system packages retain their current libraries and unversioned development links.

| File | SHA256 before package stripping |
| --- | --- |
| `libubox.so.20260523` | `6e9176aaa120cdfdb03f32552ef36213862ab0045e62189aca703ef1b367bf24` |
| `libubus.so.20260628` | `be94b248cd6444186a447b39f21b0c104a102d2f5ab2434f66d90d014abc4ae7` |

These are prebuilt compatibility components, not libraries rebuilt from this
feed. The package dependency check must remain enabled. A successful build does
not replace testing the daemon, wireless association and configuration on AIR6.
