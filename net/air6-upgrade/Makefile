include $(TOPDIR)/rules.mk

PKG_NAME:=air6-upgrade
PKG_VERSION:=1.0.0
PKG_RELEASE:=1
PKG_LICENSE:=MIT GPL-2.0-only

include $(INCLUDE_DIR)/package.mk

define Package/air6-upgrade
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=SoftBank Air 6 slot selection and signed upgrade tools
  DEPENDS:=@TARGET_mediatek_mt6990 +ucode +ucode-mod-fs +usign +jsonfilter
endef

define Build/Compile
endef

define Package/air6-upgrade/install
	$(INSTALL_DIR) $(1)/usr/sbin $(1)/lib/upgrade $(1)/usr/share/air6-cpe
	$(INSTALL_BIN) ./files/usr/sbin/air6-ui-slotctl $(1)/usr/sbin/air6-ui-slotctl
	$(INSTALL_DATA) ./files/lib/upgrade/air6-ui.sh $(1)/lib/upgrade/air6-ui.sh
	$(INSTALL_DATA) ./files/usr/share/air6-cpe/update.uc $(1)/usr/share/air6-cpe/update.uc
	if [ -f ./files/etc/air6-cpe/update.pub ]; then \
		$(INSTALL_DIR) $(1)/etc/air6-cpe; \
		$(INSTALL_DATA) ./files/etc/air6-cpe/update.pub $(1)/etc/air6-cpe/update.pub; \
	fi
endef

$(eval $(call BuildPackage,air6-upgrade))
