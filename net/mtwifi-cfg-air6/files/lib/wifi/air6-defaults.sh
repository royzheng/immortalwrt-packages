#!/bin/sh
# Repair missing fields only; preserve saved SSIDs, keys and radio choices.
. /lib/functions.sh
air6_missing() {
	local value
	config_get value "$1" "$2"
	[ -n "$value" ] && [ "$AIR6_WIRELESS_FRESH" != 1 ] || uci -q set "wireless.$1.$2=$3"
}
air6_repair_radio() {
	local section="$1" prefix band channel width phy
	config_get prefix "$section" main_ifname
	case "$prefix" in
		ra) band=2g; channel=6; width=EHT20 ;;
		rai) band=5g; channel=36; width=EHT160 ;;
		rax) band=6g; channel=37; width=EHT320 ;;
		*) return ;;
	esac
	air6_missing "$section" band "$band"
	air6_missing "$section" channel "$channel"
	air6_missing "$section" htmode "$width"
	air6_missing "$section" country CN
	if [ "$band" = 6g ]; then
		air6_missing "$section" disabled 1
	else
		air6_missing "$section" disabled 0
	fi
	phy="$(readlink -f "/sys/class/net/${prefix}0/phy80211" 2>/dev/null)"
	if [ -d "$phy" ]; then
		phy="${phy##*/}"
		[ "$(uci -q get "wireless.$section.phy")" = "$phy" ] ||
			uci -q set "wireless.$section.phy=$phy"
	fi
}
air6_repair_bss() {
	local radio
	config_get radio "$1" device
	[ "$AIR6_WIRELESS_FRESH" = 1 ] && [ "$(uci -q get "wireless.$radio.band")" = 6g ] &&
		uci -q set "wireless.$1.disabled=1"
	return 0
}
air6_repair_wireless() {
	config_load wireless
	config_foreach air6_repair_radio wifi-device
	config_foreach air6_repair_bss wifi-iface
	[ -z "$(uci -q changes wireless)" ] || uci -q commit wireless
}
