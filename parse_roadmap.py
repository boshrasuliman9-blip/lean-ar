from bs4 import BeautifulSoup
import base64

with open('index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

print('\n--- CSS ---')
for s in soup.find_all('style'):
    with open('extracted_style.css', 'w', encoding='utf-8') as fcss:
        fcss.write(s.string or '')

print('\n--- JS ---')
for s in soup.find_all('script'):
    with open('extracted_script.js', 'w', encoding='utf-8') as fjs:
        fjs.write(s.string or '')

# Extract HTML content
cards_extracted = 0

rm1 = soup.find(id='pg-roadmap')
if rm1:
    cards = rm1.find_all(class_='rm-card')
    for i, c in enumerate(cards):
        with open(f'card_{i+1}.html', 'w', encoding='utf-8') as fc:
            fc.write(str(c))
        cards_extracted += 1

rm2 = soup.find(id='pg-roadmap-2')
if rm2:
    cards = rm2.find_all(class_='rm-card')
    for i, c in enumerate(cards):
        with open(f'card_{cards_extracted + i + 1}.html', 'w', encoding='utf-8') as fc:
            fc.write(str(c))

# Extract pg-start, pg-game, pg-win
for pid in ['pg-start', 'pg-game', 'pg-win']:
    el = soup.find(id=pid)
    if el:
        with open(f'{pid}.html', 'w', encoding='utf-8') as fel:
            fel.write(str(el))
    
print("Successfully extracted files!")
