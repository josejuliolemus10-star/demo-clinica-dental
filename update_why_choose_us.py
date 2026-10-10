import os
import re
from bs4 import BeautifulSoup

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. ENCABEZADOS PRINCIPALES
    for tag in soup.find_all(string=re.compile('Why Choose Us', re.I)):
        if tag.parent and tag.parent.name == 'div':
            tag.replace_with('Por qué elegirnos')

    for h2 in soup.find_all('h2'):
        if 'We Treat You Like Family' in h2.text:
            h2.clear()
            h2.append("Te tratamos como familia, porque ")
            span = soup.new_tag('span', attrs={'class': 'text-highlighted'})
            span.string = "tu sonrisa es lo más importante"
            h2.append(span)

    # 2. ÍTEMS DEL ACORDEÓN
    replacements = {
        "Compassionate": {
            "title": "El esmalte es la sustancia más dura del cuerpo",
            "content": "Aunque tus dientes son más fuertes que tus huesos, los ácidos y el azúcar pueden desgastarlos. Nosotros te enseñamos a protegerlos para que te duren sanos toda la vida."
        },
        "Advanced Technology": {
            "title": "Producirás más de 25,000 litros de saliva",
            "content": "La saliva es tu defensa natural contra las caries. Mantener buenos hábitos y visitarnos regularmente asegura que tu boca esté siempre en perfecto equilibrio y sin dolor."
        },
        "Comprehensive Services": {
            "title": "Tu salud bucal refleja tu salud general",
            "content": "Las bacterias de las encías inflamadas pueden viajar por tu cuerpo. Cuidar tu limpieza dental con nosotros no solo salva tus dientes, sino que protege tu corazón y tu bienestar total."
        },
        "Honesty": {
            "title": "No importa cuánto tiempo haya pasado",
            "content": "Muchas personas sienten pena de ir al dentista después de años sin chequeos. Aquí no te juzgamos, estamos listos para recibirte con empatía y devolverte la salud dental sin regaños."
        },
        "Patient-Centered Care": {
            "title": "Cuentas con nosotros en cada paso",
            "content": "Sabemos que ir al dentista puede dar nervios. Por eso te explicamos todo con paciencia, usamos tecnología sin dolor y te acompañamos hasta que vuelvas a sonreír con total seguridad."
        }
    }

    for item in soup.find_all('a', class_=re.compile('tabs-accordion_item')):
        title_div = item.find('div', class_='tabs-accordion_header-title')
        if not title_div: continue
        
        orig_title = title_div.text.strip()
        for key, reps in replacements.items():
            if key in orig_title:
                # Update title
                title_div.string = reps["title"]
                
                # Update content
                info_inner = item.find('div', class_='tabs-accordion_info-inner')
                if info_inner:
                    p = info_inner.find('p')
                    if p:
                        p.string = reps["content"]
                break

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main()
