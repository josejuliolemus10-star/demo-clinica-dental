import os
import re
from bs4 import BeautifulSoup

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. TÍTULOS PRINCIPALES DE LA SECCIÓN
    for tag in soup.find_all(string=re.compile('Our Story', re.I)):
        if tag.parent and tag.parent.name == 'div':
            tag.replace_with('Nuestra Filosofía')

    for h2 in soup.find_all('h2'):
        if 'Redefining Dental' in h2.text:
            h2.clear()
            h2.append("Reinventando tu ")
            span = soup.new_tag('span', attrs={'class': 'text-highlighted'})
            span.string = "Salud Dental"
            h2.append(span)
            
            p = soup.new_tag('p', attrs={'style': 'margin-top: 15px; font-size: 18px;'})
            p.string = "Aprende, cuida y sonríe con seguridad"
            h2.insert_after(p)

    # 2. CONTENIDO DE LAS TARJETAS (CARRUSEL)
    replacements = {
        "Trusted": {
            "number": "100%",
            "text": "Única",
            "para": "Tu sonrisa es única. Al igual que tus huellas dactilares, no existen dos personas con la misma dentadura."
        },
        "Quick": {
            "number": "7",
            "text": "Minutos",
            "para": "Es el tiempo de cepillado recomendado por semana. Unos minutos al día protegen tu salud para siempre."
        },
        "Emergency": {
            "number": "Confianza",
            "text": "al Sonreír",
            "para": "Visitar al dentista te devuelve la seguridad para hablar, reír y expresarte sin timidez ni temores."
        },
        "Healthy": {
            "number": "85%",
            "text": "Hábitos",
            "para": "La gran mayoría de los problemas dentales se previene con un cepillado adecuado y visitas regulares al dentista."
        },
        "Comfort": {
            "number": "Métodos",
            "text": "Seguros",
            "para": "Atención paciente y segura. La odontología moderna utiliza técnicas para que tu cita sea una experiencia cómoda y sin dolor."
        }
    }

    cards = soup.find_all('div', class_='our-story_item')
    for card in cards:
        card_text = card.get_text()
        for key, rep in replacements.items():
            if key in card_text:
                num_div = card.find('div', class_='our-story_item-info_number')
                text_div = card.find('div', class_='our-story_item-info_text')
                title = card.find('h3', class_='our-story_item-title')
                
                if num_div: num_div.string = rep["number"]
                if text_div: text_div.string = rep["text"]
                if title: title.string = rep["para"]
                break

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main()
