import polib

# Chemins des fichiers
po_file = 'portfolio/locale/fr/LC_MESSAGES/django.po'
mo_file = 'portfolio/locale/fr/LC_MESSAGES/django.mo'

# Charger le fichier .po avec encodage UTF-8
po = polib.pofile(po_file, encoding='utf-8')

# Vérifier que l'en-tête du fichier contient bien l'encodage UTF-8
if 'charset=UTF-8' not in po.metadata.get('Content-Type', ''):
    # Ajouter ou corriger l'encodage dans les métadonnées
    po.metadata['Content-Type'] = 'text/plain; charset=UTF-8'

# Sauvegarder sous forme de fichier .mo
po.save_as_mofile(mo_file)
