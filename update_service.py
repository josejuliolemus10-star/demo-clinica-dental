import os
import re
from bs4 import BeautifulSoup

def main():
    with open('service.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. LIMPIEZA INICIAL
    for script in soup.find_all('script'):
        if script.get('src') and 'mola-widget' in script.get('src'):
            script.decompose()

    widget_html = soup.find('a', href=re.compile('mola', re.I))
    if widget_html:
        parent = widget_html.find_parent('div', class_=re.compile('fixed|absolute'))
        if parent: parent.decompose()
        else: widget_html.decompose()

    # 2. TRADUCCIÓN DEL HEADER
    p = soup.find(string=re.compile('From routine checkups to advanced treatments', re.I))
    if p:
        p_parent = p.find_parent('p')
        if p_parent:
            p_parent.string = "Desde chequeos de rutina hasta tratamientos avanzados, ofrecemos servicios dentales personalizados diseñados para mantener tu sonrisa saludable y segura."

    btn = soup.find(string=re.compile('Book An Appointment', re.I))
    if btn:
        btn.replace_with('Reservar Cita')
        a_tag = btn.find_parent('a')
        if a_tag:
            a_tag['href'] = "https://wa.me/50259790160"
            a_tag['target'] = "_blank"

    # 3. PREPARAR LA SECCIÓN DE SERVICIOS
    h2 = None
    for heading in soup.find_all('h2'):
        if 'Generation' in heading.text:
            h2 = heading
            break

    if h2:
        section = h2.find_parent('section') or h2.find_parent('div', class_=re.compile('section'))
        if section:
            # Etiqueta pequeña
            tag = section.find(string=re.compile('Our Services', re.I))
            if tag: tag.replace_with('Nuestros Servicios')

            # H2
            h2.clear()
            h2.append("Lo Que ")
            span = soup.new_tag('span', attrs={'class': 'text-highlighted'})
            span.string = "Ofrecemos"
            h2.append(span)
            h2.append(" Para Cada Generación")

            # Inline styles
            s = section.get('style', '')
            section['style'] = s + '; position: relative; overflow: hidden; max-height: 550px;' if s else 'position: relative; overflow: hidden; max-height: 550px;'

            # 4. INYECTAR EL PAYWALL
            paywall_html = '''<div style="position: absolute; top: 20%; left: 0; right: 0; bottom: 0; background: linear-gradient(to bottom, rgba(0,43,91,0) 0%, rgba(0,43,91,0.9) 40%, rgba(0,43,91,1) 100%); backdrop-filter: blur(10px); display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; z-index: 999; padding: 20px;">
  <div style="background: white; padding: 40px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.3); max-width: 500px; width: 90%; border: 3px solid #004aad;">
    <h2 style="color: #d32f2f; font-weight: bold; margin-bottom: 10px; font-size: 28px;">¡ALTO AHÍ, CURIOSO! 🛑</h2>
    <p style="color: #333; font-size: 16px; margin-bottom: 25px; line-height: 1.5;">Sabemos que te está encantando cómo luce tu clínica en este formato tan profesional...<br><br>Pero para ver la lista completa de servicios con tu información real y desbloquear la web entera... <strong>¡HAY QUE HACER TRATO!</strong> 🤝<br><br><span style="font-size: 12px; color: #888;">(P.D. No intentes usar 'Inspeccionar Elemento', borré el resto del código de verdad 😂)</span></p>
    <a href="https://wa.me/50259790160?text=Hola!%20Me%20rindo,%20la%20p%C3%A1gina%20se%20ve%20genial.%20%C2%BFHacemos%20trato?" target="_blank" style="background: #25D366; color: white; padding: 15px 30px; border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 18px; display: inline-block; transition: 0.3s;">¡Contratar Ahora por WhatsApp!</a>
  </div>
</div>'''
            paywall_soup = BeautifulSoup(paywall_html, 'html.parser')
            section.append(paywall_soup)

            # 5. LA EJECUCIÓN FINAL (A prueba de hackers)
            next_sibling = section.find_next_sibling()
            while next_sibling:
                to_delete = next_sibling
                next_sibling = next_sibling.find_next_sibling()
                if to_delete.name and to_delete.name != 'script':
                    to_delete.decompose()

            # The section is probably inside a <main> tag. We also need to delete siblings of <main>
            main_tag = section.find_parent('main')
            if main_tag:
                next_main_sibling = main_tag.find_next_sibling()
                while next_main_sibling:
                    to_delete = next_main_sibling
                    next_main_sibling = next_main_sibling.find_next_sibling()
                    if to_delete.name and to_delete.name != 'script':
                        to_delete.decompose()

    with open('service.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main()
