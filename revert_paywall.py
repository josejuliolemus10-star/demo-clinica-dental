import os
import re
from bs4 import BeautifulSoup

def main():
    with open('about.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. ELIMINAR EL BLOQUEO (PAYWALL)
    msg_box = soup.find(string=re.compile('¡ALTO AHÍ!'))
    if msg_box:
        paywall_container = msg_box.find_parent('div').find_parent('div')
        if paywall_container and 'backdrop-filter' in paywall_container.get('style', ''):
            paywall_container.decompose()

    # Quitar el position relative de parent de la img si fue modificado
    img = soup.find('img', class_='about-hero_image')
    if img:
        container = img.find_parent('div')
        if container:
            s = container.get('style', '')
            if 'position: relative' in s or 'overflow: hidden' in s:
                s = s.replace('position: relative;', '').replace('overflow: hidden;', '').strip()
                if not s:
                    del container['style']
                else:
                    container['style'] = s

    # 2. RESTAURAR EL SCROLL
    # En lugar de solo buscar los hermanos, voy a buscar cualquier section o footer 
    # que tenga 'display: none' y se lo quitaré (ya que la página original no los ocultaba).
    for tag in soup.find_all(['section', 'footer', 'div']):
        style = tag.get('style', '')
        if 'display: none' in style:
            # Eliminar la regla de display: none
            new_style = re.sub(r'display:\s*none;?', '', style).strip()
            if not new_style:
                del tag['style']
            else:
                tag['style'] = new_style

    with open('about.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main()
