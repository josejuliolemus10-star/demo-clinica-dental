import os
import re
from bs4 import BeautifulSoup

def main():
    with open('about.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Find the section
    team_section = None
    for h2 in soup.find_all('h2'):
        if 'Superheroes' in h2.text:
            team_section = h2.find_parent('section') or h2.find_parent('div', class_='section_component')
            
            # Update H2
            h2.clear()
            h2.append("Los Superhéroes Detrás de tu ")
            span = soup.new_tag('span', attrs={'class': 'text-highlighted'})
            span.string = "Cuidado Dental"
            h2.append(span)
            break
            
    if team_section:
        # Paragraph
        for p in team_section.find_all('p'):
            if 'Each member of our clinical staff' in p.text:
                p.string = "Cada miembro de nuestro equipo clínico no solo está altamente calificado, sino profundamente comprometido con brindarte la mejor atención y ayudarte a lograr una sonrisa perfecta."

        # 6 Doctor cards
        items = team_section.find_all('div', class_='team_item')
        for item in items:
            # Update Image
            img = item.find('img', class_='team_image')
            if img:
                img['src'] = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'
                if 'srcset' in img.attrs:
                    del img['srcset']
                    
            # Update Name
            name = item.find(['h2', 'h3'], class_='team-menmber_name')
            if name:
                name.string = "Aquí irá el doctor especializado"
                
            # Update Designation
            desig = item.find('p', class_='team-menuber_designation')
            if desig:
                desig.string = "Especialidad Médica"

    with open('about.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main()
