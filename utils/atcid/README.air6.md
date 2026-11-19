# Retained ATCI SDK sources

This directory preserves the former `package/mtk/atcid` source material and its NOTICE. The source tree did not contain a top-level OpenWrt package Makefile; the nested `atci/src/Makefile` and `atci_service/src/Makefile` are SDK build files, with SDK-specific dependencies.

No new package buildability is claimed by this relocation. The current runtime `atcid`/`atci_service` binaries are supplied by `net/air6-modem-chain-only`. Keep the source material here for future replacement work without introducing a second package that installs conflicting runtime binaries.
