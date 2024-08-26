from pathlib import Path
import re
import shutil
from datetime import datetime

def process_markdown(input_file: Path):
    content = input_file.read_text(encoding='utf-8')
    
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
        content = re.sub(r'^#\s+.+\n', '', content, 1)
    else:
        print("Title not found in the file.")
        return
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    new_file_name = f"{date_str}-{'-'.join(title.split()[:3]).lower()}.md"
    new_file_path = Path('..') / '_posts' / new_file_name
    
    header = f"""---
layout: post
title: "{title}"
---
"""
    content = header + content
    
    image_dir = input_file.with_suffix('')
    if image_dir.is_dir():
        new_image_dir = Path('..') / 'assets' / 'images' / '-'.join(title.split()[:3]).lower()
        print(new_image_dir)
        new_image_dir.mkdir(parents=True, exist_ok=True)
        
        for img in image_dir.iterdir():
            if img.is_file():
                shutil.move(str(img), str(new_image_dir / img.name))
        
        content = re.sub(
            r'!\[(.+?)\]\((.+?)\)',
            lambda m: f'![](assets/images/{"-".join(title.split()[:3]).lower()}/{Path(m.group(2)).name}){{:style="display:block; margin-left:auto; margin-right:auto"}}',
            content
        )
    
    new_file_path.write_text(content, encoding='utf-8')
    
    print(f"Processing completed. New file created: {new_file_path}")
    input_file.unlink()
    print(f"Original file deleted: {input_file}")
    
    if image_dir.is_dir():
        shutil.rmtree(image_dir)
        print(f"Original image folder deleted: {image_dir}")

# Script usage
input_file = Path(input("Enter the name of the Markdown file to process: "))
process_markdown(input_file)