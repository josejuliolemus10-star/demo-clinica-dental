import os
import re
from bs4 import BeautifulSoup

def main():
    with open('about.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. SECTION CTA
    cta = soup.find('section', class_=re.compile('section_cta', re.I))
    if cta:
        # Tag
        tag = cta.find(string=re.compile('Get In Touch', re.I))
        if tag: tag.replace_with('Contáctanos')

        # H2
        for h2 in cta.find_all('h2'):
            if 'Talk Teeth' in h2.text:
                h2.clear()
                h2.append("Hablemos de tu salud, estamos a ")
                span = soup.new_tag('span', attrs={'class': 'text-highlighted'})
                span.string = "una sonrisa de distancia"
                h2.append(span)

        # Paragraph
        for p in cta.find_all('p'):
            if 'Your health journey' in p.text:
                p.string = "Tu camino hacia una boca sana comienza con un simple paso. Estamos aquí para guiarte en todo momento."

        # Button
        btn = cta.find(string=re.compile('Get Started', re.I))
        if btn:
            btn.replace_with('Agendar por WhatsApp')
            a = btn.find_parent('a')
            if a:
                a['href'] = "https://wa.me/50259790160"
                a['target'] = "_blank"

    # 2. FOOTER
    footer = soup.find('footer', class_=re.compile('footer', re.I))
    if footer:
        # Phone
        phone = footer.find(string=re.compile('0114 317 7002', re.I))
        if phone: phone.replace_with('5979-0160')

        # Paragraph
        p = footer.find('p', class_='footer-info_para')
        if p and 'Advanced technology' in p.text:
            p.string = "Tecnología avanzada y un equipo humano con tratamientos diseñados para mantener tu sonrisa sana para toda la vida en Centro Médico Villa Nueva."

        # Button
        btn_appt = footer.find(string=re.compile('Get Appointment', re.I))
        if btn_appt:
            btn_appt.replace_with('Agendar Cita')
            a = btn_appt.find_parent('a')
            if a:
                a['href'] = "https://wa.me/50259790160"
                a['target'] = "_blank"

        # 3. ENLACES SECUNDARIOS
        cols = footer.find_all('div', class_='footer-links-column')
        
        # Col 1: Navigation
        if len(cols) > 0:
            title = cols[0].find('div', class_='footer-menu_title')
            if title and 'Navigation' in title.text:
                title.string = "Navegación"
            
            links = cols[0].find_all('a')
            nav_texts = ["Inicio", "Nosotros", "Servicios", "Consejos"]
            for idx, a in enumerate(links):
                a['href'] = "#"
                if idx < len(nav_texts):
                    div = a.find('div')
                    if div: div.string = nav_texts[idx]
                else:
                    a.decompose()
        
        # Col 2: Legal
        if len(cols) > 1:
            title = cols[1].find('div', class_='footer-menu_title')
            if title and 'Legal' in title.text:
                title.string = "Legal"
            
            links = cols[1].find_all('a')
            leg_texts = ["Términos y Condiciones", "Cookies", "Privacidad"]
            for idx, a in enumerate(links):
                a['href'] = "#"
                if idx < len(leg_texts):
                    div = a.find('div')
                    if div: div.string = leg_texts[idx]
                else:
                    a.decompose()

        # Col 3: Follow us
        if len(cols) > 2:
            title = cols[2].find('div', class_='footer-menu_title')
            if title and 'Follow us' in title.text:
                title.string = "Redes Sociales"
            
            links = cols[2].find_all('a')
            for a in links:
                a['href'] = "#"

    with open('about.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main()
