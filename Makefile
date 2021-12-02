
.PHONY: build
build: web/venv/docker

# *** *** Python dependencies *** ***

# Créer un virtual env
web/venv/bin/activate:
	cd web; python3 -m venv venv/

# Installer les dépendances
# Pour forcer la mise à jour, il suffit de modifier le fichier requirements.txt ou de supprimer le marqueur 'venv/installed'
web/venv/install: web/venv/bin/activate web/requirements.txt
	cd web; . venv/bin/activate; pip install -r requirements.txt
	touch web/venv/installed  # marqueur pour éviter de télécharger les dépendances à chaque fois

# Mettre à jour le fichier 'requirements.txt' après avoir fait un 'pip install' ou similaire
.PHONY: web/commit-dependencies
web/commit-dependencies: web/venv/bin/activate
	cd web; . venv/bin/activate; pip freeze >requirements.txt

# *** *** Python Coding style *** ***

# Vérifie que le code respecte le coding style
.PHONY: lint
web/lint: web/venv/install
	cd web; . venv/bin/activate; pycodestyle --show-source --show-pep8 --statistics --benchmark --max-line-length=120 . --exclude=venv/

# *** *** JavaScript interface *** ***

node=docker run --rm --mount type=bind,source="$(shell pwd)/web-ui",target=/app node:alpine

/tmp/node_pull:
	docker pull node:alpine
	touch /tmp/node_pull

web-ui/node_modules: /tmp/node_pull web-ui/package.json
	$(node) sh -c 'cd /app && yarn --color=always && touch node_modules'

js_sources=$(shell find web-ui/js)
css_sources=$(shell find web-ui/css)
web-ui/dist: /tmp/node_pull web-ui/node_modules $(js_sources) $(css_sources)
	$(node) sh -c 'cd /app && yarn --color=always build'

ui_dist=$(shell find web-ui/dist -type f)
web/src/static: web-ui/dist $(ui_dist)
	cp -r web-ui/dist web/src/static
	touch "$@"

images_dist=$(shell find web-ui/images -type f)
web/src/static/images: $(images_dist)
	cp -r web-ui/images web/src/static/images

# *** *** Server image *** ***

web/venv/docker: web/src/static web/src/static/images web/requirements.txt web web/venv/bin/activate web/src
	docker build -t ctf-platform:latest web
	touch web/venv/docker

.PHONY: start
start: web/venv/docker
	docker-compose up -d

.PHONY: stop
stop:
	docker-compose down

.PHONY: cli
cli: start
	docker-compose exec server bash

# *** *** Cleanup *** ***

.PHONY: web/clean
web/clean:
	rm -rf web/src/static web/venv

.PHONY: web-ui/clean
web-ui/clean:
	sudo rm -rf web-ui/node_modules web-ui/dist

.PHONY: clean
clean: web/clean web-ui/clean
	sudo rm -rf data
	@echo "To cleanup Docker files, you might want to run 'docker system prune'"
