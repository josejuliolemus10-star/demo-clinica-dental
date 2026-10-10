import os
import re
from bs4 import BeautifulSoup

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. ENCABEZADO DE LA SECCIÓN
    for tag in soup.find_all(string=re.compile('Our Services', re.I)):
        if tag.parent and tag.parent.name == 'div':
            tag.replace_with('Nuestros Servicios')
    
    for h2 in soup.find_all('h2'):
        if 'Comprehensive Dental Care' in h2.text:
            h2.clear()
            h2.append("Cuidado Dental Integral para ")
            span = soup.new_tag('span', attrs={'class': 'text-highlighted'})
            span.string = "Cada Sonrisa"
            h2.append(span)
            
    for p in soup.find_all('p'):
        if 'we combine expertise, compassion' in p.text:
            p.string = "En Especialistas Dentales Integrados, combinamos experiencia, empatía y tecnología moderna para ofrecer una atención que nuestros pacientes realmente valoran."

    for btn in soup.find_all(string=re.compile('See All Services', re.I)):
        btn.replace_with("Ver Todos los Servicios")

    # 2. BOTONES DE LAS TARJETAS
    for btn in soup.find_all(string=re.compile('View Details', re.I)):
        btn.replace_with("Ver Detalles")

    # 3. ETIQUETAS FLOTANTES (PILLS)
    pills_map = {
        "Teeth Whitening": "Blanqueamiento",
        "Whitening": "Blanqueamiento",
        "Dental Veneers": "Carillas Dentales",
        "Smile Makeover": "Diseño de Sonrisa",
        "Cosmetic Bonding": "Resinas Estéticas",
        "Dental Health": "Salud Dental",
        "Dental Implants": "Implantes",
        "Checkups": "Salud Dental",
        "Dental Fillings": "Resinas Estéticas"
    }

    # Find all pills
    for pill in soup.find_all('div', class_=re.compile('service-item_tag', re.I)):
        # The text is in a div inside pill, not the icon
        for inner_div in pill.find_all('div'):
            # Ignore the icon div
            if 'service-tag_icon' in inner_div.get('class', []):
                continue
                
            text = inner_div.text.strip()
            if not text:
                continue
                
            for eng, spa in pills_map.items():
                if eng.lower() in text.lower():
                    inner_div.string = spa
                    break

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main()
