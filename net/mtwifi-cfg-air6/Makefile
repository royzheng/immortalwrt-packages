include $(TOPDIR)/rules.mk

PKG_NAME:=mtwifi-cfg-air6
PKG_VERSION:=1.0.0
PKG_RELEASE:=3

# Personal build component: the mtwifi bring-up set (ubus daemon + netifd
# wireless scripts + first-boot detect + stock wireless defaults) extracted
# from the maintainer's signed softbank_air6 b8c232a6 update bundle on the
# build host. The public openwrt-air6 tree deliberately ships without this
# component; this package restores it for private builds of this device.
# Upstream lineage: mtwifi-cfg-tool (oraybox / StarField Xu et al., GPL).

include $(INCLUDE_DIR)/package.mk

define Package/mtwifi-cfg-air6
  SECTION:=firmware
  CATEGORY:=Firmware
  TITLE:=AIR6 mtwifi wireless bring-up (from maintainer bundle)
  DEPENDS:=+libubus +libubox +libuci +libjson-c +libgcc \
    +hostapd-openssl +hostapd-utils +iw +jshn +wifi-scripts +kmod-mt7990-wifi
endef

define Package/mtwifi-cfg-air6/description
 Replaces the standard mac80211 netifd wireless handler with the AIR6
 mtwifi one: /usr/sbin/mtwifi ubus daemon, /etc/init.d/mtwifi procd
 service (global hostapd control socket + first-boot UCI detect),
 /lib/netifd/wireless/mac80211.sh and /lib/wifi/mt_dbdc.sh netifd
 glue, plus stock tri-band /etc/config/wireless defaults
 (Air6-2.4G / Air6-5G / Air6-6G, country CN; 6 GHz disabled).
endef

define Package/mtwifi-cfg-air6/conffiles
/etc/config/wireless
endef

define Build/Compile
endef

define Package/mtwifi-cfg-air6/install
	$(INSTALL_DIR) $(1)/usr/sbin $(1)/usr/lib $(1)/etc/init.d $(1)/etc/config \
		$(1)/lib/netifd/wireless $(1)/lib/wifi $(1)/usr/libexec
	# Keep the prebuilt daemon's exact ABI libraries alongside current system libs.
	$(INSTALL_DATA) ./files/usr/lib/libubox.so.20260523 $(1)/usr/lib/
	$(INSTALL_DATA) ./files/usr/lib/libubus.so.20260628 $(1)/usr/lib/
	$(INSTALL_BIN) ./files/usr/libexec/air6-wireless-status $(1)/usr/libexec/
	$(INSTALL_DATA) ./files/lib/wifi/air6-defaults.sh $(1)/lib/wifi/
	$(INSTALL_BIN) ./files/usr/sbin/mtwifi $(1)/usr/sbin/mtwifi
	$(INSTALL_BIN) ./files/etc/init.d/mtwifi $(1)/etc/init.d/mtwifi
	$(INSTALL_DATA) ./files/etc/config/wireless $(1)/etc/config/wireless
	$(INSTALL_BIN) ./files/lib/netifd/wireless/mac80211.sh $(1)/lib/netifd/wireless/mac80211.sh
	$(INSTALL_BIN) ./files/lib/wifi/mt_dbdc.sh $(1)/lib/wifi/mt_dbdc.sh
endef

$(eval $(call BuildPackage,mtwifi-cfg-air6))
