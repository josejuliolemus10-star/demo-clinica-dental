import os
import re
from bs4 import BeautifulSoup

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. ENCABEZADOS PRINCIPALES
    for tag in soup.find_all(string=re.compile('Testimonials', re.I)):
        if tag.parent and tag.parent.name == 'div':
            tag.replace_with('Testimonios')
            
    # "Voices of Trust and Care" -> "Lo que dicen nuestros pacientes"
    for h2 in soup.find_all('h2'):
        if 'Voices of' in h2.text or 'Trust and Care' in h2.text:
            h2.clear()
            h2.append("Lo que dicen")
            br = soup.new_tag('br')
            h2.append(br)
            span = soup.new_tag('span', attrs={'class': 'text-highlighted'})
            span.string = "nuestros pacientes"
            h2.append(span)

    # 2. TARJETAS DEL CARRUSEL
    testimonials_data = [
        {
            "name": "Stefano Girón",
            "text": "Excelente servicio en todos los aspectos. El equipo es muy profesional, atento y amable."
        },
        {
            "name": "Brenda Mariana",
            "text": "Muy buen servicio, las secretarias muy amables al explicar el procedimiento."
        },
        {
            "name": "Paciente Verificado",
            "text": "Atención de primera y un ambiente seguro. Cuentan con parqueo y las instalaciones están impecables."
        }
    ]

    cards = soup.find_all('div', class_='testimonial-slider_card')
    for idx, card in enumerate(cards):
        if idx >= len(testimonials_data):
            break
        
        data = testimonials_data[idx]
        
        author_div = card.find('div', class_='testimonial-slider_author')
        if author_div:
            author_div.clear()
            
            # Recreate image wrap
            img_wrap = soup.new_tag('div', attrs={'class': 'testimonial-author_image-wrap'})
            img = soup.new_tag('img', attrs={
                'class': 'testimonial-author_image',
                'loading': 'lazy',
                'src': 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png',
                'alt': 'Testimonial image'
            })
            img_wrap.append(img)
            
            # Recreate info wrap
            info_wrap = soup.new_tag('div', attrs={'class': 'testimonial-author_info'})
            name_h3 = soup.new_tag('h3', attrs={'class': 'testimonial-author_name'})
            name_h3.string = data["name"]
            
            stars_div = soup.new_tag('div', attrs={
                'class': 'testimonial-author_designation',
                'style': 'color: #FFD700; font-size: 16px; margin-top: 4px; letter-spacing: 2px;'
            })
            stars_div.string = "⭐⭐⭐⭐⭐"
            
            info_wrap.append(name_h3)
            info_wrap.append(stars_div)
            
            author_div.append(img_wrap)
            author_div.append(info_wrap)
            
        quotes_wrap = card.find('div', class_='testimonial-slider_quotes-wrap')
        if quotes_wrap:
            p = quotes_wrap.find('p')
            if p:
                p.string = data["text"]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main()
