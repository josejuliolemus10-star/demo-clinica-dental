import os
import re
from bs4 import BeautifulSoup

def main():
    with open('about.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. MEJORAR EL DEGRADADO Y EL BLUR
    msg_box = soup.find(string=re.compile('¡ALTO AHÍ!'))
    if msg_box:
        paywall_container = msg_box.find_parent('div').find_parent('div')
        if paywall_container and 'backdrop-filter' in paywall_container.get('style', ''):
            style = paywall_container['style']
            
            # Replace background
            style = re.sub(
                r'background:\s*linear-gradient[^;]+;', 
                'background: linear-gradient(to bottom, rgba(255,255,255,0) 0%, rgba(255,255,255,0.2) 35%, rgba(255,255,255,0.75) 70%, rgba(255,255,255,1) 100%);', 
                style
            )
            
            # Replace blur
            style = re.sub(
                r'blur\([^\)]+\)', 
                'blur(12px)', 
                style
            )
            
            paywall_container['style'] = style

    # 2. CORTAR LA PÁGINA (Bloquear el scroll)
    img = soup.find('img', class_='about-hero_image')
    if img:
        hero_section = img.find_parent('section') or img.find_parent('div', class_=re.compile('section'))
        if hero_section:
            # Hide all siblings inside main
            next_sibling = hero_section.find_next_sibling()
            while next_sibling:
                if next_sibling.name and next_sibling.name != 'script':
                    s = next_sibling.get('style', '')
                    if 'display: none' not in s:
                        next_sibling['style'] = s + '; display: none;' if s else 'display: none;'
                next_sibling = next_sibling.find_next_sibling()

            # Hide everything after <main>
            main_tag = hero_section.find_parent('main')
            if main_tag:
                next_main_sibling = main_tag.find_next_sibling()
                while next_main_sibling:
                    if next_main_sibling.name and next_main_sibling.name != 'script':
                        s = next_main_sibling.get('style', '')
                        if 'display: none' not in s:
                            next_main_sibling['style'] = s + '; display: none;' if s else 'display: none;'
                    next_main_sibling = next_main_sibling.find_next_sibling()

    with open('about.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main()
