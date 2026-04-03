import os

# Clean up extracted_style.css duplicates
with open('extracted_style.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

# We know the first part is duplicated starting around the second `* { box-sizing:border-box;`
idx = css_content.find('* { box-sizing:border-box; margin:0; padding:0; }', 10)
if idx != -1:
    css_content = css_content[:idx]

with open('extracted_style.css', 'w', encoding='utf-8') as f:
    f.write(css_content.strip())

# Clean up other abandoned scripts
obsolete_files = [
    'edit_game_logic.py',
    'edit_roadmap_kids.py',
    'edit_win.py',
    'fix_game_buttons.py',
    'update_images.py',
    'update_index.py',
    'extracted_script.js',
    'java.js'
]

for file in obsolete_files:
    if os.path.exists(file):
        os.remove(file)

print("Cleanup complete!")
