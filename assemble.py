import os

with open('extracted_style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add dynamic themes and pagination
# We use a LIGHTER color for border/button and DARKER color for drop shadow!
css += """

/* --- Dynamic Themes --- */

/* Page 1 Theme: Sunny Orange */
.theme-1 .rm-card { border-color: #f59e0b; box-shadow: 0 8px 0px #b45309; }
.theme-1 .rm-arrow { color: #f59e0b; text-shadow: 0 3px 0px #b45309; }
.theme-1 .btn-next { background: #f59e0b; box-shadow: 0 8px 0px #b45309; }
.theme-1 .btn-next:active { box-shadow: 0 0px 0px #b45309; transform: translateY(8px); }

/* Page 2 Theme: Fun Purple */
.theme-2 .rm-card { border-color: #8b5cf6; box-shadow: 0 8px 0px #6d28d9; }
.theme-2 .rm-arrow { color: #8b5cf6; text-shadow: 0 3px 0px #6d28d9; }
.theme-2 .btn-next { background: #8b5cf6; box-shadow: 0 8px 0px #6d28d9; }
.theme-2 .btn-next:active { box-shadow: 0 0px 0px #6d28d9; transform: translateY(8px); }

/* Page 3 Theme: Green / Mint */
.theme-3 .rm-card { border-color: #10b981; box-shadow: 0 8px 0px #059669; }
.theme-3 .rm-arrow { color: #10b981; text-shadow: 0 3px 0px #059669; }
.theme-3 .btn-next { background: #10b981; box-shadow: 0 8px 0px #059669; }
.theme-3 .btn-next:active { box-shadow: 0 0px 0px #059669; transform: translateY(8px); }

/* --- Pagination --- */
.pagination { display: flex; justify-content: center; gap: 8px; margin-bottom: 24px; }
.dot { width: 14px; height: 14px; border-radius: 50%; background: #ccc; transition: 0.3s; }
.dot.active { transform: scale(1.3); }
.theme-1 .dot.active { background: #f59e0b; }
.theme-2 .dot.active { background: #8b5cf6; }
.theme-3 .dot.active { background: #10b981; }
"""

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# HTML Templates
head_template = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Roadmap</title>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
"""

def make_page(filename, theme_num, title, active_dot, cards_files, button_text, button_link):
    cards_html = ""
    for cf in cards_files:
        with open(cf, 'r', encoding='utf-8') as f:
            cards_html += f.read() + '''
            <div class="rm-arrow">↓</div>
            '''

    dots_html = ""
    for i in range(1, 4):
        active = " active" if i == active_dot else ""
        dots_html += f'<div class="dot{active}"></div>'

    html = head_template + f"""
<div id="pg-roadmap" class="theme-{theme_num}">
  <h2>🗺️ {title}</h2>
  <div class="pagination">
    {dots_html}
  </div>
  <div class="rm-wrap">
    {cards_html}
  </div>
  <a href="{button_link}" class="btn-next">{button_text}</a>
</div>
</body>
</html>
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

make_page('index.html', 1, 'المعرفة والتعلم', 1, ['card_1.html', 'card_2.html'], 'التالي', 'roadmap2.html')
make_page('roadmap2.html', 2, 'التركيب والبرمجة', 2, ['card_3.html', 'card_4.html'], 'التالي', 'roadmap3.html')
make_page('roadmap3.html', 3, 'المتعة والتحدي', 3, ['card_5.html', 'card_6.html'], 'ابدا اللعبة', 'game.html')

with open('pg-start.html', 'r', encoding='utf-8') as f:
    start_html = f.read()
with open('pg-game.html', 'r', encoding='utf-8') as f:
    game_html = f.read()
with open('pg-win.html', 'r', encoding='utf-8') as f:
    win_html = f.read()

# Make start block always visible
start_html = start_html.replace('display:none;', 'display:block;')

with open('game.html', 'w', encoding='utf-8') as f:
    f.write(head_template + start_html + game_html + win_html + '''
<script src="game.js"></script>
</body>
</html>''')

print("Pages created & assembled fully!")
