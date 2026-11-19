#!/bin/sh
#
# Legacy "/lib/wifi" detect plugin for the MediaTek stack managed by this
# program (installed as /lib/wifi/mt_dbdc.sh).
#
# /sbin/wifi sources every /lib/wifi/*.sh and collects the names registered
# through `append DRIVERS`. The classic "wifi config" path then runs the
# matching detect_<name>() for each of them. Registering "mt_dbdc" here makes
# that path generate an "mt_dbdc" configuration, instead of letting
# detect_mac80211() claim the MediaTek PHYs: the MTK stack exposes its radios
# through cfg80211 as well, so a generic mac80211 detect adds bogus
# `type mac80211` wifi-devices for the very same PHYs.
#
# This matters because /sbin/wifi config is invoked by the mac80211
# ieee80211-subsystem hotplug (/etc/hotplug.d/ieee80211/10-wifi-detect) on every
# PHY add, i.e. during boot as well.

append DRIVERS "mt_dbdc"

detect_mt_dbdc() {
	local dev type
	local have_mtk=0 have_mac80211=0

	# Only when this program owns the radios on this board.
	[ -x /lib/netifd/wireless/mac80211.sh ] || return 0
	[ -x /usr/sbin/mtwifi ] || return 0
	[ -s /etc/wireless/l1profile.dat ] || return 0

	# The netifd shim is installed as mac80211.sh and the radios carry
	# "type mac80211": an existing configuration is ours, never rewrite it.
	if grep -q 'add_driver mac80211' /lib/netifd/wireless/mac80211.sh 2>/dev/null &&
	   uci -q show wireless | grep -q '=wifi-device$'; then
		return 0
	fi

	for dev in $(uci -q show wireless |
		sed -n 's/^wireless\.\([^.]*\)=wifi-device$/\1/p'); do
		type=$(uci -q get "wireless.$dev.type")
		case "$type" in
		mt_dbdc|mtkwifi) have_mtk=1 ;;
		mac80211) have_mac80211=1 ;;
		esac
	done

	# Nothing to do when the config already describes the MTK radios and no
	# generic device sneaked in; this keeps later detect runs from resetting
	# user edits.
	[ "$have_mtk" = 1 ] && [ "$have_mac80211" = 0 ] && return 0

	# One-shot takeover, run only while the config is not ours yet:
	#  - drop the mac80211 hotplug so a later PHY add never re-runs
	#    "/sbin/wifi config" and overwrites user edits (disabled interfaces)
	#  - drop the mac80211 netifd driver so the MTK PHYs are never claimed by it
	# Both removals are permanent (overlay), which is intended on MTK boards.
	[ -e "/etc/hotplug.d/ieee80211/10-wifi-detect" ] &&
		rm -f /etc/hotplug.d/ieee80211/10-wifi-detect
	# mac80211.sh is our shim; never delete it.

	# Rebuild the whole UCI wireless config from the driver profiles (dat2uci
	# equivalent). Write to a temporary file first so a failed detect never
	# leaves an empty /etc/config/wireless behind.
	rm -f /tmp/wireless.mt_dbdc
	if /usr/sbin/mtwifi detect /tmp/wireless.mt_dbdc; then
		sed -i "s/option type 'mt_dbdc'/option type 'mac80211'/" /tmp/wireless.mt_dbdc
		mv -f /tmp/wireless.mt_dbdc /etc/config/wireless
	else
		rm -f /tmp/wireless.mt_dbdc
		return 1
	fi
}
