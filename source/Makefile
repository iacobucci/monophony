prefix = /usr

SHELL = bash
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

INSTALL = install -D
ID = io.gitlab.zehkira.Monophony
ICONS_DIR = $(prefix)/share/icons/hicolor
LOCALES_DIR = $(prefix)/share/locale
APPS_DIR = $(prefix)/share/applications
META_DIR = $(prefix)/share/metainfo
LICENSE_DIR = $(prefix)/share/licenses
BIN_DIR = $(prefix)/bin


install:
	@# Executable
	$(INSTALL) bin/monophony.py $(BIN_DIR)/monophony

	@# Desktop file
	$(INSTALL) data/monophony.desktop $(APPS_DIR)/$(ID).desktop

	@# Metainfo
	$(INSTALL) data/metainfo.xml $(META_DIR)/$(ID).metainfo.xml

	@# Icons
	$(INSTALL) data/icons/scalable.svg $(ICONS_DIR)/scalable/apps/$(ID).svg
	$(INSTALL) \
		data/icons/symbolic.svg $(ICONS_DIR)/symbolic/apps/$(ID)-symbolic.svg
	$(INSTALL) data/icons/128.png $(ICONS_DIR)/128x128/apps/$(ID).png
	$(INSTALL) data/icons/16.png $(ICONS_DIR)/16x16/apps/$(ID).png
	$(INSTALL) data/icons/192.png $(ICONS_DIR)/192x192/apps/$(ID).png
	$(INSTALL) data/icons/22.png $(ICONS_DIR)/22x22/apps/$(ID).png
	$(INSTALL) data/icons/24.png $(ICONS_DIR)/24x24/apps/$(ID).png
	$(INSTALL) data/icons/256.png $(ICONS_DIR)/256x256/apps/$(ID).png
	$(INSTALL) data/icons/32.png $(ICONS_DIR)/32x32/apps/$(ID).png
	$(INSTALL) data/icons/36.png $(ICONS_DIR)/36x36/apps/$(ID).png
	$(INSTALL) data/icons/384.png $(ICONS_DIR)/384x384/apps/$(ID).png
	$(INSTALL) data/icons/48.png $(ICONS_DIR)/48x48/apps/$(ID).png
	$(INSTALL) data/icons/512.png $(ICONS_DIR)/512x512/apps/$(ID).png
	$(INSTALL) data/icons/64.png $(ICONS_DIR)/64x64/apps/$(ID).png
	$(INSTALL) data/icons/72.png $(ICONS_DIR)/72x72/apps/$(ID).png
	$(INSTALL) data/icons/96.png $(ICONS_DIR)/96x96/apps/$(ID).png

	@# Translations
	cd locales; \
	for d in */; do \
		$(INSTALL) \
			$${d}LC_MESSAGES/all.mo $(LOCALES_DIR)/$${d}LC_MESSAGES/monophony.mo; \
	done

	@# License
	$(INSTALL) LICENSE $(LICENSE_DIR)/monophony/LICENSE
.PHONY: install


# For testing purposes - builds and installs a flatpak
flatpak:
	flatpak --version
	flatpak-builder --version

	flatpak remote-add \
		--user \
		--if-not-exists \
		flathub \
		https://dl.flathub.org/repo/flathub.flatpakrepo
	flatpak-builder \
		--user \
		--install \
		--install-deps-from=flathub \
		--force-clean \
		--repo=repo/ \
		build/ \
		data/manifest.json
.PHONY: flatpak


# Updates the trasnslation template
translation:
	printf 'msgid \"\"\nmsgstr \"Content-Type: text/plain; charset=UTF-8\\n\"' \
		> locales/all.pot
	find monophony -iname "*.py" | xargs xgettext --omit-header -j -o locales/all.pot
.PHONY: translation
