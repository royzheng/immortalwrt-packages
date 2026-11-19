include $(TOPDIR)/rules.mk

PKG_NAME:=mihomo
PKG_VERSION:=1.19.34
PKG_RELEASE:=1
PKG_LICENSE:=GPL-3.0-only
PKG_SOURCE:=mihomo-linux-arm64-v$(PKG_VERSION).gz
PKG_SOURCE_URL:=https://github.com/MetaCubeX/mihomo/releases/download/v$(PKG_VERSION)/
PKG_HASH:=daaf78a6240a282cdfd75bcbf98fe321f6bd52765cc29e79f344191198f0b50f

include $(INCLUDE_DIR)/package.mk

define Package/mihomo
  SECTION:=net
  CATEGORY:=Network
  TITLE:=Mihomo Meta core (pinned upstream ARM64 build)
  URL:=https://github.com/MetaCubeX/mihomo
  DEPENDS:=@aarch64 +ca-bundle
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	gzip -dc $(DL_DIR)/$(PKG_SOURCE) > $(PKG_BUILD_DIR)/mihomo
endef

define Build/Configure
endef
define Build/Compile
endef

define Package/mihomo/install
	$(INSTALL_DIR) $(1)/usr/bin $(1)/usr/share/mihomo $(1)/etc/openclash/core
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/mihomo $(1)/usr/bin/mihomo
	$(INSTALL_DATA) ./LICENSE ./SOURCE.md $(1)/usr/share/mihomo/
	$(LN) /usr/bin/mihomo $(1)/etc/openclash/core/clash_meta
endef

$(eval $(call BuildPackage,mihomo))
