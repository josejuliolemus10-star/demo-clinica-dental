import os
from bs4 import BeautifulSoup
import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. ELIMINAR WIDGET DE IA Y CREAR BOTÓN FLOTANTE DE WHATSAPP
    # Find and remove the script
    for script in soup.find_all('script'):
        src = script.get('src', '')
        if 'mola-widget' in src:
            script.decompose()

    # Append WhatsApp button before </body>
    whatsapp_html = """
    <a href="https://wa.me/50259790160" target="_blank" style="position: fixed; bottom: 20px; right: 20px; background-color: #25D366; color: white; border-radius: 50px; padding: 10px 20px; font-weight: bold; text-decoration: none; z-index: 9999; box-shadow: 0px 4px 10px rgba(0,0,0,0.3); display: flex; align-items: center; gap: 8px;">
      💬 Escríbenos al WhatsApp
    </a>
    """
    body = soup.find('body')
    if body:
        # Avoid adding it multiple times if script runs multiple times
        # Let's check if it already exists
        if not soup.find('a', string=re.compile('Escríbenos al WhatsApp')):
            new_btn = BeautifulSoup(whatsapp_html, 'html.parser')
            body.append(new_btn)

    # 2. MODIFICAR LOS 3 CUADROS DE INFORMACIÓN
    info_boxes = soup.find_all('div', class_='our-info_item')
    if len(info_boxes) >= 3:
        # Box 0 (Left)
        box0 = info_boxes[0]
        title0 = box0.find('h2', class_='our-info_title')
        if title0: title0.string = "Agenda tu Cita"
        
        # The paragraph is usually inside a link or just a div
        para0 = box0.find('div', class_='our-info_item-para')
        if para0:
            para0.string = "¿Listo para una sonrisa más sana? Agenda tu visita hoy."
            
        # Box 1 (Center)
        box1 = info_boxes[1]
        title1 = box1.find('h2', class_='our-info_title')
        if title1: title1.string = "Contacto y Parqueo"
        
        paras1 = box1.find_all('div', class_='our-info_item-para')
        if len(paras1) >= 2:
            paras1[0].string = "5979-0160"
            paras1[1].string = "claudiamarissac@gmail.com"
        
        # Check if parking info already added
        if not box1.find(string=re.compile('Parqueo seguro y gratuito')):
            body1 = box1.find('div', class_='our-info_item-body')
            if body1:
                parking_html = '<div class="our-info_item-para" style="margin-top: 10px;">🚗 Parqueo seguro y gratuito para pacientes.</div>'
                body1.append(BeautifulSoup(parking_html, 'html.parser'))

        # Box 2 (Right)
        box2 = info_boxes[2]
        title2 = box2.find('h2', class_='our-info_title')
        if title2: title2.string = "Horarios de Atención"
        
        paras2 = box2.find_all('div', class_='our-info_item-para')
        # They are typically in pairs inside .our-info_block
        if len(paras2) >= 4:
            paras2[0].string = "Lun - Vie"
            paras2[1].string = "8:00 - 17:00"
            paras2[2].string = "Sábado"
            paras2[3].string = "8:00 - 12:00"

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == "__main__":
    main()
