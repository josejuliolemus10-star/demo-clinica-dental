import os
import re
from bs4 import BeautifulSoup

def main():
    with open('about.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Find the awards section
    section = soup.find('section', class_='section_awards')
    if section:
        # 1. LOS 4 CUADROS SUPERIORES (Pestañas/Botones)
        links = section.find_all('a', class_=re.compile('awards-tabs_link'))
        texts_tabs = [
            "Aquí colocaremos",
            "Lo que tu negocio",
            "Nos pida. Si te gusta...",
            "¡CONTRÁTANOS!"
        ]
        
        for idx, link in enumerate(links):
            if idx < len(texts_tabs):
                # The text is usually inside a div
                # Look for a div inside the link that actually contains text
                for div in link.find_all('div'):
                    if div.text.strip() and not div.find('img') and not div.find('svg'):
                        div.string = texts_tabs[idx]
                        break

        # 2. ENCABEZADOS Y PÁRRAFO PRINCIPAL (This is repeated in each tab pane)
        panes = section.find_all('div', class_=re.compile('awards-tabs_pane'))
        for pane in panes:
            # Tag small
            tag = pane.find(string=re.compile('Awards & Recognition', re.I))
            if tag:
                if tag.parent.name == 'div':
                    tag.replace_with('Tu Espacio a Medida')

            # H2
            h2 = pane.find('h2')
            if h2 and 'Honored' in h2.text:
                h2.clear()
                h2.append("Imagina tus Logros o Servicios ")
                span = soup.new_tag('span', attrs={'class': 'text-highlighted'})
                span.string = "Destacados Aquí"
                h2.append(span)

            # Paragraph
            p = pane.find('p', class_='body-text-18px')
            if p and 'Our commitment to innovation' in p.text:
                p.string = "Este espacio está reservado exclusivamente para presumir lo que hace única a tu clínica. ¿Te gusta cómo se ve esta estructura profesional? Aquí colocaremos exactamente lo que tu negocio necesite. Así que, si te interesa verla funcionando con tu información real... ¡contrátanos y hagamos trato!"

            # 3. LOS 3 PUNTOS DE LISTA
            items = pane.find_all('div', class_='awards-tabs_pane-feature_item')
            bullets = [
                "Personalizamos cada rincón de esta web según tus necesidades.",
                "Destacamos tus mejores servicios para atraer más pacientes.",
                "Si quieres ver la magia completa, ¡escríbenos al WhatsApp!"
            ]
            for idx, item in enumerate(items):
                if idx < len(bullets):
                    # El texto está en un div hermano al del SVG
                    divs = item.find_all('div', recursive=False)
                    if len(divs) >= 2:
                        divs[1].string = bullets[idx]

            # 4. TEXTO DENTRO DE LA IMAGEN
            h3 = pane.find('h3', class_='awards-tabs_image-content_title')
            if h3 and 'National Dental Association' in h3.text:
                h3.string = "Espacio 100% Disponible"

    with open('about.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main()
