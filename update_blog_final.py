import os
import re
from bs4 import BeautifulSoup

def main():
    with open('blog.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. HEADER WIDGET & BUTTON
    # Remove AI script
    for script in soup.find_all('script'):
        if script.get('src') and 'mola-widget' in script.get('src'):
            script.decompose()

    # Change Header button
    btn = soup.find(string=re.compile('Get Appointment', re.I))
    if btn:
        btn.replace_with('Agendar Cita')
        a_tag = btn.find_parent('a')
        if a_tag:
            a_tag['href'] = "https://wa.me/50259790160"
            a_tag['target'] = "_blank"

    # 2. FUNCIONALIDAD DEL BOTÓN "LEER COMPLETO"
    feat = soup.find('div', class_=re.compile('feature-blog_content', re.I))
    if feat:
        # Insert the hidden container
        desc = feat.find('p', class_=re.compile('feature-blog_text', re.I))
        if desc:
            html_snippet = '''<div id="tipsCepillado" style="display: none; margin-top: 15px; padding-top: 15px; border-top: 1px solid #e5e7eb;">
    <h4 style="margin-bottom: 10px; color: #002B5B; font-weight: bold;">4 Pasos para un cepillado perfecto:</h4>
    <ul style="list-style-type: disc; padding-left: 20px; color: #4b5563; line-height: 1.6;">
      <li><strong>Cerdas suaves:</strong> Usa un cepillo de cerdas suaves para no dañar tu esmalte ni irritar tus encías.</li>
      <li><strong>Regla de los 2 minutos:</strong> Cepilla tus dientes por lo menos dos veces al día durante dos minutos completos.</li>
      <li><strong>Técnica de barrido:</strong> Cepilla desde la encía hacia el borde del diente (de arriba hacia abajo en los superiores, y viceversa).</li>
      <li><strong>Limpia tu lengua:</strong> Ahí se acumulan las bacterias que causan el mal aliento. Cepíllala suavemente.</li>
    </ul>
  </div>'''
            tips_soup = BeautifulSoup(html_snippet, 'html.parser')
            desc.insert_after(tips_soup)
            
        # Update button functionality
        rm = feat.find(string=re.compile('Leer completo', re.I))
        if rm:
            a_tag = rm.find_parent('a')
            if a_tag:
                a_tag['href'] = "#"
                a_tag['onclick'] = "event.preventDefault(); var x = document.getElementById('tipsCepillado'); var txt = this.querySelector('.button_text'); if (x.style.display === 'none') { x.style.display = 'block'; txt.innerHTML = 'Ocultar'; } else { x.style.display = 'none'; txt.innerHTML = 'Leer completo'; }"
                if 'target' in a_tag.attrs:
                    del a_tag['target']

    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main()
