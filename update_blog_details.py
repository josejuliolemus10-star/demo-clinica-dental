import os
import re
from bs4 import BeautifulSoup

def main():
    # ------------------ INDEX.HTML ------------------
    with open('index.html', 'r', encoding='utf-8') as f:
        soup_index = BeautifulSoup(f.read(), 'html.parser')
    
    # 3 cards in 'Consejos Prácticos' section
    blog_section = soup_index.find('section', class_=re.compile('section_blog', re.I))
    if blog_section:
        cards = blog_section.find_all('a', class_=re.compile('blog_item', re.I))
        for card in cards:
            card['href'] = 'blog.html'
            if 'target' in card.attrs:
                del card['target']
                
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup_index))


    # ------------------ BLOG.HTML ------------------
    with open('blog.html', 'r', encoding='utf-8') as f:
        soup_blog = BeautifulSoup(f.read(), 'html.parser')
        
    # H1
    for h1 in soup_blog.find_all('h1'):
        if 'Insights' in h1.text:
            h1.string = "Consejos para una Sonrisa más Sana"
            
    # Subtitle
    for p in soup_blog.find_all('p', class_='body-text-18px'):
        if 'From everyday habits' in p.text:
            p.string = "Desde hábitos diarios hasta tratamientos avanzados, nuestros expertos comparten información valiosa para cuidar tu salud bucal."

    # FEATURED CARD
    feat = soup_blog.find('div', class_=re.compile('feature-blog_content', re.I))
    if feat:
        # Preventive Care -> Cuidado Preventivo
        tag = feat.find(string=re.compile('Preventive Care', re.I))
        if tag: tag.replace_with('Cuidado Preventivo')
        
        # Oral Health Tips -> Salud Bucal
        info = feat.find(string=re.compile('Oral Health Tips', re.I))
        if info: info.replace_with('Salud Bucal')
        
        # April 30, 2026 -> 15 de Mayo, 2026
        date = feat.find(string=re.compile('April', re.I))
        if date: date.replace_with('15 de Mayo, 2026')
        
        # Title
        title = feat.find(['h2', 'h3'], class_=re.compile('feature-blog_title'))
        if title: title.string = "La guía definitiva para el cepillado: ¿Lo estás haciendo bien?"
        
        # Text
        desc = feat.find('p', class_=re.compile('feature-blog_text'))
        if desc: desc.string = "Descubre los secretos de una buena técnica de cepillado y cómo mantener tus dientes fuertes y libres de caries desde casa. Te explicamos paso a paso lo que debes hacer."
        
        # Read More
        rm = feat.find(string=re.compile('Read More', re.I))
        if rm: rm.replace_with('Leer completo')
        
    # BOTTOM CARDS
    bottom_cards = soup_blog.find_all('a', class_=re.compile('blog_item', re.I))
    
    # TIP 2
    if len(bottom_cards) > 0:
        c1 = bottom_cards[0]
        t1 = c1.find(['h2', 'h3'], class_=re.compile('blog-item_title'))
        if t1: t1.string = "Mitos dentales: Lo que tus dientes realmente necesitan para estar sanos."
        
        # Insert <p> below title
        p1 = soup_blog.new_tag('p', attrs={'style': 'margin-top: 10px; font-size: 16px; color: #555;'})
        p1.string = "Desmentimos los remedios caseros falsos y te enseñamos la verdad respaldada por la ciencia para cuidar tus dientes."
        if t1.parent:
            t1.insert_after(p1)
            
        rm1 = c1.find(string=re.compile('Read More', re.I))
        if rm1: rm1.replace_with('Leer completo')

    # TIP 3
    if len(bottom_cards) > 1:
        c2 = bottom_cards[1]
        t2 = c2.find(['h2', 'h3'], class_=re.compile('blog-item_title'))
        if t2: t2.string = "La verdad sobre el hilo dental: Por qué usarlo no es opcional."
        
        p2 = soup_blog.new_tag('p', attrs={'style': 'margin-top: 10px; font-size: 16px; color: #555;'})
        p2.string = "El cepillado no basta. Aprende cómo el uso diario del hilo dental previene enfermedades en las encías y evita la pérdida de dientes."
        if t2.parent:
            t2.insert_after(p2)
            
        rm2 = c2.find(string=re.compile('Read More', re.I))
        if rm2: rm2.replace_with('Leer completo')
        
    # Delete remaining cards
    for idx in range(2, len(bottom_cards)):
        parent = bottom_cards[idx].find_parent('div', role='listitem')
        if parent: parent.decompose()
        else: bottom_cards[idx].decompose()

    # WHATSAPP BUTTON
    wa_html = '''<a href="https://wa.me/50259790160" target="_blank" style="position: fixed; bottom: 20px; right: 20px; background-color: #25D366; color: white; border-radius: 50px; padding: 10px 20px; font-weight: bold; text-decoration: none; z-index: 9999; box-shadow: 0px 4px 10px rgba(0,0,0,0.3); display: flex; align-items: center; gap: 8px;">
    💬 Escríbenos al WhatsApp
  </a>'''
    wa_soup = BeautifulSoup(wa_html, 'html.parser')
    
    # Remove AI widget if it was somehow remaining
    widget = soup_blog.find('a', href=re.compile('mola'))
    if widget:
        parent = widget.find_parent('div', class_=re.compile('fixed|absolute'))
        if parent: parent.decompose()
        else: widget.decompose()
        
    body = soup_blog.find('body')
    if body:
        body.append(wa_soup)

    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(str(soup_blog))

if __name__ == '__main__':
    main()
