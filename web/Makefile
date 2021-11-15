run:

# *** Dependencies ***

# Créer un virtual env
venv/bin/activate:
	python3 -m venv venv/

# Installer les dépendances
# Pour forcer la mise à jour, il suffit de modifier le fichier requirements.txt ou de supprimer le marqueur 'venv/installed'
venv/install: venv/bin/activate requirements.txt
	. venv/bin/activate && pip install -r requirements.txt
	touch venv/install  # marqueur pour éviter de télécharger les dépendances à chaque fois

# Mettre à jour le fichier 'requirements.txt' après avoir fait un 'pip install' ou similaire
.PHONY: commit-dependencies
commit-dependencies: venv/bin/activate
	. venv/bin/activate && pip freeze >requirements.txt

# *** Coding style ***

# Vérifie que le code respecte le coding style
.PHONY: lint
lint: venv/install
	. venv/bin/activate && pycodestyle --show-source --show-pep8 --statistics --benchmark --max-line-length=120 . --exclude=venv/
