from pathlib import Path
import re
import shutil
from datetime import datetime

def process_markdown(input_file: Path):
    # Lire le contenu du fichier
    content = input_file.read_text(encoding='utf-8')
    
    # Extraire le titre
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
        # Supprimer le titre original du contenu
        content = re.sub(r'^#\s+.+\n', '', content, 1)
    else:
        print("Titre non trouvé dans le fichier.")
        return
    
    # Créer le nouveau nom de fichier
    date_str = datetime.now().strftime('%Y-%m-%d')
    new_file_name = f"{date_str}-{'-'.join(title.split()[:3]).lower()}.md"
    new_file_path = Path('../_posts') / new_file_name
    
    # Ajouter l'en-tête au contenu
    header = f"""---
layout: post
title: "{title}"
---
"""
    content = header + content
    
    # Traiter les images
    image_dir = input_file.with_suffix('')
    if image_dir.is_dir():
        new_image_dir = Path('..') / 'assets' / 'images' / '-'.join(title.split()[:3]).lower()
        new_image_dir.mkdir(parents=True, exist_ok=True)
        
        for img in image_dir.iterdir():
            if img.is_file():
                shutil.move(str(img), str(new_image_dir / img.name))
        
        # Mettre à jour les liens d'images dans le contenu
        content = re.sub(
            r'!\[(.+?)\]\((.+?)\)',
            lambda m: f'![](/assets/images/{"-".join(title.split()[:3]).lower()}/{Path(m.group(2)).name}){{:style="display:block; margin-left:auto; margin-right:auto"}}',
            content
        )
    
    # Écrire le nouveau fichier avec tout le contenu traité
    new_file_path.write_text(content, encoding='utf-8')
    
    print(f"Traitement terminé. Nouveau fichier créé : {new_file_path}")

# Utilisation du script
input_file = Path(input("Entrez le nom du fichier Markdown à traiter : "))
process_markdown(input_file)