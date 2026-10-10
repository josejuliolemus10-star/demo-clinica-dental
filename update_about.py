import os
import re
from bs4 import BeautifulSoup

def main():
    with open('about.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. LIMPIEZA DEL WIDGET DE IA
    for script in soup.find_all('script'):
        if script.get('src') and 'mola-widget' in script.get('src'):
            script.decompose()

    widget_html = soup.find('a', href=re.compile('mola', re.I))
    if widget_html:
        parent = widget_html.find_parent('div', class_=re.compile('fixed|absolute'))
        if parent: parent.decompose()
        else: widget_html.decompose()

    # 2. TRADUCCIÓN Y AJUSTE DE DATOS
    h1 = soup.find(['h1', 'h2'], string=re.compile('Trusted Dental Experts', re.I))
    if h1:
        h1.string = "Expertos Dentales de Confianza, Décadas de Cuidado"

    # Párrafo
    p = soup.find(string=re.compile('compassion, innovation, and expertise', re.I))
    if p:
        p_parent = p.find_parent('p')
        if p_parent:
            p_parent.string = "En Especialistas Dentales Integrados, combinamos compasión, innovación y experiencia para brindar una atención en la que puedes confiar. Tu sonrisa es nuestra prioridad."

    # Botón
    btn = soup.find(string=re.compile('Book An Appointment', re.I))
    if btn:
        btn.replace_with('Reservar Cita')
        a_tag = btn.find_parent('a')
        if a_tag:
            a_tag['href'] = "https://wa.me/50259790160"
            a_tag['target'] = "_blank"

    # Estadísticas
    stat1_num = soup.find(string=re.compile('25\+', re.I))
    if stat1_num: stat1_num.replace_with('20+')
    
    stat1_text = soup.find(string=re.compile('Years of Dental Excellence', re.I))
    if stat1_text: stat1_text.replace_with('Años de Experiencia')

    stat2_num = soup.find(string=re.compile('10k\+', re.I))
    if stat2_num: stat2_num.replace_with('+500')
    
    stat2_text = soup.find(string=re.compile('Smiles Transformed', re.I))
    if stat2_text: stat2_text.replace_with('Tratamientos Realizados')

    # 3. EFECTO DE BLOQUEO "PAYWALL"
    img = soup.find('img', class_='about-hero_image')
    if img:
        container = img.find_parent('div')
        if container:
            # Add relative and overflow hidden
            style = container.get('style', '')
            if 'position' not in style:
                style += '; position: relative;'
            if 'overflow' not in style:
                style += '; overflow: hidden;'
            container['style'] = style

            paywall_html = '''<div style="position: absolute; top: 30%; left: 0; right: 0; bottom: 0; background: linear-gradient(to bottom, rgba(255,255,255,0) 0%, rgba(255,255,255,0.8) 40%, rgba(255,255,255,1) 100%); backdrop-filter: blur(6px); display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; z-index: 50; padding: 20px;">
  <div style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.15); max-width: 400px; width: 90%; margin-top: 50px;">
    <h2 style="color: #004aad; font-weight: bold; margin-bottom: 15px;">¡ALTO AHÍ! 🛑</h2>
    <p style="color: #333; font-size: 18px; margin-bottom: 20px;">Si quieres ver cómo queda el resto de la página funcionando... <strong>¡CONTRÁTANOS!</strong> 😉</p>
    <a href="https://wa.me/50259790160?text=Hola!%20Me%20encant%C3%B3%20la%20prueba%20de%20la%20p%C3%A1gina.%20%C2%BFHacemos%20trato?" target="_blank" style="background: #004aad; color: white; padding: 12px 24px; border-radius: 50px; text-decoration: none; font-weight: bold; display: inline-block;">¡Hagamos trato por WhatsApp!</a>
  </div>
</div>'''
            paywall_soup = BeautifulSoup(paywall_html, 'html.parser')
            img.insert_after(paywall_soup)

            # Opcional: Eliminar todo lo que esté debajo de esta sección
            hero_section = container.find_parent('section') or container.find_parent('div', class_=re.compile('section'))
            if hero_section:
                next_sibling = hero_section.find_next_sibling()
                while next_sibling:
                    to_delete = next_sibling
                    next_sibling = next_sibling.find_next_sibling()
                    # only decompose structural elements like sections and footers, leaving script tags if any
                    if to_delete.name in ['section', 'footer', 'div'] and to_delete.get('class') != 'script':
                        to_delete.decompose()

    with open('about.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main()
