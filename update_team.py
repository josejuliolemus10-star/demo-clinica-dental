import os
import re
from bs4 import BeautifulSoup

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. ENCABEZADO DE LA SECCIÓN
    # Update H2
    for h2 in soup.find_all('h2'):
        if 'Our' in h2.text and 'Experts' in h2.text and 'in Oral Health' in h2.text:
            h2.clear()
            h2.append("Nuestros ")
            span = soup.new_tag('span', attrs={'class': 'text-highlighted'})
            span.string = "Expertos"
            h2.append(span)
            h2.append(" en Salud Bucal")

    # Update paragraph
    for p in soup.find_all('p', class_='home-team_header-para'):
        if 'Each member of our clinical staff' in p.text:
            p.string = "Cada miembro de nuestro equipo clínico está altamente calificado y comprometido con brindarte la mejor atención."
        # Just in case the text was already translated or partially cut off, replace it unconditionally if it's the home-team header para
        else:
            # Let's verify it by checking the parent section just to be safe
            parent = p.find_parent('div', class_='home-team_header')
            if parent:
                p.string = "Cada miembro de nuestro equipo clínico está altamente calificado y comprometido con brindarte la mejor atención."

    # 2. TARJETAS DE DOCTORES
    for card in soup.find_all('div', class_=re.compile('team_item')):
        img = card.find('img', class_='team_image')
        if img:
            img['src'] = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'
            if img.has_attr('srcset'): del img['srcset']
            if img.has_attr('sizes'): del img['sizes']

        name = card.find('h3', class_='team-menmber_name')
        if name:
            name.string = "Aquí irá el doctor especializado"

        desig = card.find('p', class_='team-menuber_designation')
        if desig:
            desig.string = "Especialidad Médica"

    # 3. BOTÓN INFERIOR
    btn_text = soup.find(string=re.compile('View All Doctors', re.I))
    if btn_text:
        parent_a = btn_text.find_parent('a')
        btn_text.replace_with("Contáctanos")
        if parent_a:
            parent_a['href'] = "https://wa.me/50259790160"
            parent_a['target'] = "_blank"

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main()
