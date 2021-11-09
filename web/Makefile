run:

# Créer un virtual env
venv/bin/activate:
	python3 -m venv venv/

# Installer les dépendances
# Pour forcer la mise à jour, il suffit de modifier le fichier requirements.txt ou de supprimer le marqueur 'venv/installed'
venv/installed: venv/bin/activate requirements.txt
	. venv/bin/activate && pip install -r requirements.txt
	touch venv/installed  # marqueur pour éviter de télécharger les dépendances à chaque fois

# Mettre à jour le fichier 'requirements.txt' après avoir fait un 'pip install' ou similaire
.PHONY: commit-dependencies
commit-dependencies: venv/bin/activate
	. venv/bin/activate && pip freeze >requirements.txt
