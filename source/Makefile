prefix = /usr

SHELL = bash
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

INSTALL_PROGRAM = install -D
INSTALL_DATA = install -D -m 644
ID = io.gitlab.zehkira.Monophony
NAME = monophony
BIN_DIR = $(prefix)/bin
DATA_DIR = $(prefix)/share
ICONS_DIR = $(DATA_DIR)/icons/hicolor
LOCALES_DIR = $(DATA_DIR)/locale
APPS_DIR = $(DATA_DIR)/applications
META_DIR = $(DATA_DIR)/metainfo
LICENSE_DIR = $(DATA_DIR)/licenses


# Only use for packaging. For manual builds, see "flatpak" instead
install:
	@# Python module
	pip3 install --prefix=$(prefix) --no-build-isolation --no-deps .

	@# Executable
	$(INSTALL_PROGRAM) bin/$(NAME).py $(BIN_DIR)/$(NAME)

	@# GResources
	mkdir --parents $(DATA_DIR)/$(NAME)
	glib-compile-resources \
		--sourcedir=data \
		--target=$(DATA_DIR)/$(NAME)/resources.gresource \
		data/resources.gresource.xml

	@# Desktop file
	$(INSTALL_DATA) data/$(NAME).desktop $(APPS_DIR)/$(ID).desktop

	@# Metainfo
	$(INSTALL_DATA) data/metainfo.xml $(META_DIR)/$(ID).metainfo.xml

	@# Icons
	$(INSTALL_DATA) data/icons/scalable.svg $(ICONS_DIR)/scalable/apps/$(ID).svg
	$(INSTALL_DATA) \
		data/icons/symbolic.svg $(ICONS_DIR)/symbolic/apps/$(ID)-symbolic.svg
	$(INSTALL_DATA) data/icons/128.png $(ICONS_DIR)/128x128/apps/$(ID).png
	$(INSTALL_DATA) data/icons/16.png $(ICONS_DIR)/16x16/apps/$(ID).png
	$(INSTALL_DATA) data/icons/192.png $(ICONS_DIR)/192x192/apps/$(ID).png
	$(INSTALL_DATA) data/icons/22.png $(ICONS_DIR)/22x22/apps/$(ID).png
	$(INSTALL_DATA) data/icons/24.png $(ICONS_DIR)/24x24/apps/$(ID).png
	$(INSTALL_DATA) data/icons/256.png $(ICONS_DIR)/256x256/apps/$(ID).png
	$(INSTALL_DATA) data/icons/32.png $(ICONS_DIR)/32x32/apps/$(ID).png
	$(INSTALL_DATA) data/icons/36.png $(ICONS_DIR)/36x36/apps/$(ID).png
	$(INSTALL_DATA) data/icons/384.png $(ICONS_DIR)/384x384/apps/$(ID).png
	$(INSTALL_DATA) data/icons/48.png $(ICONS_DIR)/48x48/apps/$(ID).png
	$(INSTALL_DATA) data/icons/512.png $(ICONS_DIR)/512x512/apps/$(ID).png
	$(INSTALL_DATA) data/icons/64.png $(ICONS_DIR)/64x64/apps/$(ID).png
	$(INSTALL_DATA) data/icons/72.png $(ICONS_DIR)/72x72/apps/$(ID).png
	$(INSTALL_DATA) data/icons/96.png $(ICONS_DIR)/96x96/apps/$(ID).png

	@# Translations
	cd locales; \
	for d in */; do \
		mkdir --parents $(LOCALES_DIR)/$${d}LC_MESSAGES/; \
		msgfmt \
			$${d}LC_MESSAGES/all.po \
			--output-file $(LOCALES_DIR)/$${d}LC_MESSAGES/$(NAME).mo; \
	done

	@# Dependency license data
	$(INSTALL_DATA) data/licenses.json $(DATA_DIR)/$(NAME)/licenses.json

	@# License
	cd ..; \
		$(INSTALL_DATA) LICENSE $(LICENSE_DIR)/$(NAME)/LICENSE
.PHONY: install


# For testing purposes - builds and installs a flatpak
flatpak:
	@flatpak --version
	@flatpak-builder --version

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
		--repo=.repo/ \
		.build/ \
		data/manifest.json
.PHONY: flatpak


# Updates the trasnslation template
translation:
	printf 'msgid \"\"\nmsgstr \"Content-Type: text/plain; charset=UTF-8\\n\"' \
		> locales/all.pot
	git ls-files \
		| grep ".py$$" \
		| xargs xgettext --no-location --omit-header -j -o locales/all.pot
.PHONY: translation


define DOCS_TEMPLATE
{%- block content %}
	{% block body %} {% endblock %}
{%- endblock %}
endef
export DOCS_TEMPLATE

define DOCS_CONFIG
html_theme = 'basic'
html_theme_options = {'nosidebar': 'true'}
html_permalinks = False
html_show_sourcelink = False
html_show_copyright = False
html_show_sphinx = False
endef
export DOCS_CONFIG

define DOCS_CLEANUP_SCRIPT
import re

with open('.docbuild/_build/index.html', 'r+') as file:
	text = file.read()

	# Remove hyperlinks
	for match in re.findall('<a.*?internal.*?>.*?<\\/a>', text, flags=re.MULTILINE):
		text = text.replace(
			match, re.sub('<a.*?>', '', match, count=1).removesuffix('</a>')
		)

	# Remove useless tag pairs, double newlines and surrounding whitespace
	text = re.sub('<[^\\/>]*><\\/[^>]*>', '', text).replace('\n\n', '\n').strip()

	file.seek(0)
	file.write('<!-- Auto-generated, do not edit -->\n' + text + '\n')
	file.truncate()
endef
export DOCS_CLEANUP_SCRIPT

define DOCS_GENERATION_SCRIPT
rm -rf .docbuild

python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip3 install -r requirements-doc.txt
sphinx-apidoc -o .docbuild --full --module-first -a $(NAME)
echo "$$DOCS_TEMPLATE" >> .docbuild/_templates/layout.html
echo "$$DOCS_CONFIG" >> .docbuild/conf.py
sed -n -i '/.. toctree::/,$$p' .docbuild/index.rst
PYTHONPATH="$$PYTHONPATH:$$(pwd)" sphinx-build \
	--builder singlehtml \
	.docbuild/ \
	.docbuild/_build/
deactivate

python3 -c "$$DOCS_CLEANUP_SCRIPT"
cp .docbuild/_build/index.html ../docs/REFERENCE.md
endef
export DOCS_GENERATION_SCRIPT

# Generates docs for the currently installed app version
docs:
	echo "$$DOCS_GENERATION_SCRIPT" | flatpak run \
		--command="sh" \
		--filesystem="$$(dirname $$(pwd))" \
		--env=MONOPHONY_LOG_LEVELS=Error \
		$(ID)
.PHONY: docs
