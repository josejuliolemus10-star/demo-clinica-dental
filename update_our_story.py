import os
import re
from bs4 import BeautifulSoup

def main():
    with open('about.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. ENCABEZADOS PRINCIPALES
    tag = soup.find(string=re.compile('Our Story', re.I))
    if tag:
        tag.replace_with('Nuestra Historia')

    for h2 in soup.find_all('h2'):
        if 'Journey' in h2.text:
            h2.clear()
            h2.append("Un Camino de Cuidado Dental, Construido con ")
            span = soup.new_tag('span', attrs={'class': 'text-highlighted'})
            span.string = "Empatía e Innovación"
            h2.append(span)
            h2.append(" para ti")

    # 2. PÁRRAFO DESCRIPTIVO
    p = soup.find(string=re.compile('Mola has been dedicated', re.I))
    if p:
        p_parent = p.find_parent('p')
        if p_parent:
            p_parent.string = "En Especialistas Dentales Integrados nos dedicamos a transformar vidas a través de sonrisas saludables. Te garantizamos la mejor atención desde el primer momento, brindándote tratamientos seguros, tecnología moderna y un equipo humano en el que tú y tu familia pueden confiar plenamente."

    # 3. BOTÓN DE ACCIÓN
    btn = soup.find(string=re.compile('Learn More', re.I))
    if btn:
        btn.replace_with('Escríbenos')
        a_tag = btn.find_parent('a')
        if a_tag:
            a_tag['href'] = "https://wa.me/50259790160"
            a_tag['target'] = "_blank"

    with open('about.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main()
