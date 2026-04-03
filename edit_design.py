import os

# 1. Update extracted_style.css
with open('extracted_style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Make desktop cards smaller
css = css.replace("""  .rm-card {
    max-width: 600px; 
    flex: 1 1 400px;
    margin: 0;
  }""", """  .rm-card {
    max-width: 480px; 
    flex: 1 1 300px;
    margin: 0;
  }""")

# Upgrade rules-box to be bubbly and cute
css = css.replace(""".rules-box { background:#fff; border:1px solid #ddd; border-radius:14px; padding:1.2rem 1.4rem; text-align:right; margin-bottom:1.5rem; }""", """.rules-box { background:#fff; border:4px solid #10b981; border-radius:24px; box-shadow:0 6px 0px #34d399; padding:1.2rem 1.4rem; text-align:right; margin-bottom:1.5rem; }""")

# Make the announce modal rules box bubbly too!
css = css.replace("""#announce {
  display:none; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
  background:rgba(20,20,20,.88); color:#fff; border-radius:18px;
  padding:24px 32px; text-align:center; font-size:20px; font-weight:700;
  line-height:1.6; z-index:30; min-width:240px;
}""", """#announce {
  display:none; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
  background:#fff; color:#1a1a1a; 
  border:5px solid #10b981; border-radius:24px; box-shadow:0 8px 0px #34d399;
  padding:24px 32px; text-align:center; font-size:20px; font-weight:700;
  line-height:1.6; z-index:30; min-width:320px;
}""")

with open('extracted_style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 2. Add class="theme-3" to game wrappers so buttons get bouncy theme styles
# pg-game.html
with open('pg-game.html', 'r', encoding='utf-8') as f:
    pg_game = f.read()
if '<div id="pg-game"' in pg_game and 'class="theme-3"' not in pg_game:
    pg_game = pg_game.replace('<div id="pg-game"', '<div id="pg-game" class="theme-3"')
with open('pg-game.html', 'w', encoding='utf-8') as f:
    f.write(pg_game)

# pg-win.html
with open('pg-win.html', 'r', encoding='utf-8') as f:
    pg_win = f.read()
if '<div id="pg-win"' in pg_win and 'class="theme-3"' not in pg_win:
    pg_win = pg_win.replace('<div id="pg-win"', '<div id="pg-win" class="theme-3"')
with open('pg-win.html', 'w', encoding='utf-8') as f:
    f.write(pg_win)

print("Design modifications applied!")
