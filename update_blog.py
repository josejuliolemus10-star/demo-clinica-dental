import os
import re
from bs4 import BeautifulSoup

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. ENCABEZADOS PRINCIPALES
    for tag in soup.find_all(string=re.compile('Blogs', re.I)):
        if tag.parent and tag.parent.name == 'div':
            tag.replace_with('Consejos')

    for h2 in soup.find_all('h2'):
        if 'Stories and Tips' in h2.text or 'Around the World' in h2.text:
            h2.clear()
            h2.append("Consejos Prácticos Para Cuidar ")
            span = soup.new_tag('span', attrs={'class': 'text-highlighted'})
            span.string = "Tu Sonrisa"
            h2.append(span)

    # Boton superior
    btn_text = soup.find(string=re.compile('See All Blogs', re.I))
    if btn_text:
        parent_a = btn_text.find_parent('a')
        btn_text.replace_with("Ver más consejos")
        if parent_a:
            parent_a['href'] = "https://wa.me/50259790160"
            parent_a['target'] = "_blank"

    # 2. TARJETAS DE TIPS
    blog_data = [
        {
            "text": "Mitos dentales: Lo que tus dientes realmente necesitan para estar sanos.",
            "href": "https://wa.me/50259790160?text=Hola,%20me%20gustar%C3%ADa%20saber%20m%C3%A1s%20sobre%20los%20mitos%20dentales%20que%20vi%20en%20su%20p%C3%A1gina."
        },
        {
            "text": "La verdad sobre el hilo dental: Por qué usarlo no es opcional.",
            "href": "https://wa.me/50259790160?text=Hola,%20me%20interesa%20el%20tip%20sobre%20el%20uso%20correcto%20del%20hilo%20dental."
        },
        {
            "text": "La guía definitiva para el cepillado: ¿Lo estás haciendo bien?",
            "href": "https://wa.me/50259790160?text=Hola,%20quiero%20conocer%20la%20gu%C3%ADa%20definitiva%20para%20un%20buen%20cepillado."
        }
    ]

    cards = soup.find_all('a', class_=re.compile('blog_item', re.I))
    for idx, card in enumerate(cards):
        if idx >= len(blog_data):
            break
        
        data = blog_data[idx]
        
        # Enlaces de la tarjeta principal
        card['href'] = data["href"]
        card['target'] = "_blank"
            
        # Titulo de la tarjeta
        title = card.find(['h2', 'h3', 'h4'], class_=re.compile('blog-item_title'))
        if title:
            title.string = data["text"]
            
        # También traducir "Read More"
        read_more = card.find(string=re.compile('Read More', re.I))
        if read_more:
            read_more.replace_with("Leer Más")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main()
