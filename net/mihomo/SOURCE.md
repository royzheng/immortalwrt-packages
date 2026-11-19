# Pinned upstream core

- Upstream: https://github.com/MetaCubeX/mihomo
- Release: v1.19.34, source commit `0455d0d28c4526937380505153e65a843d8612e8`
- Corresponding source: https://github.com/MetaCubeX/mihomo/tree/0455d0d28c4526937380505153e65a843d8612e8
- Release archive: `mihomo-linux-arm64-v1.19.34.gz`
- SHA256: `daaf78a6240a282cdfd75bcbf98fe321f6bd52765cc29e79f344191198f0b50f`
- License: GPL-3.0-only; upstream LICENSE is installed with the core.
- Local changes: packaging only, no binary/source modification. OpenWrt may strip ELF during packaging; record the installed hash independently.
- OpenClash uses `/etc/openclash/core/clash_meta`, initially a symlink to `/usr/bin/mihomo`.
- GeoIP/GeoSite databases are optional and not bundled. Offline configs must use explicit domain/IP/MATCH rules and contain no remote providers, GEOIP or GEOSITE references. Configurations requesting those resources need separately obtained and verified data.
- No subscription, credentials, enabled proxy or automatic core update is installed.
