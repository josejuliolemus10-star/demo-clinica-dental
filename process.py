import os
import glob
import re
from bs4 import BeautifulSoup

def process_file():
    html_files = glob.glob('*.html')
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')

        # PASO 2: Limpieza Destructiva
        for el in soup.find_all(string=re.compile(r'\$85/hr|85\/hr', re.I)):
            try:
                section = el.find_parent('section') or el.find_parent('div', class_=re.compile(r'section', re.I))
                if section: section.decompose()
            except AttributeError: pass
        
        for el in soup.find_all(string=re.compile(r'across the USA', re.I)):
            try:
                section = el.find_parent('section') or el.find_parent('div', class_=re.compile(r'section', re.I))
                if section: section.decompose()
            except AttributeError: pass

        stats_found = False
        for el in soup.find_all(string=re.compile(r'50K\+ Patient Visits')):
            try:
                section = el.find_parent('section') or el.find_parent('div', class_=re.compile(r'section', re.I))
            except AttributeError: section = None
            if section and not stats_found:
                stats_found = True
                new_html = """
                <div class="container" style="display: flex; flex-wrap: wrap; align-items: center; gap: 2rem; padding: 4rem 0;">
                    <div style="flex: 1; min-width: 300px;">
                        <h2>Odontopediatría: Cuidamos la sonrisa de los más pequeños</h2>
                        <p>Sabemos que la primera visita al dentista es crucial. Ofrecemos un ambiente seguro y amigable para que tus hijos pierdan el miedo al dentista.</p>
                        <a href="https://wa.me/50259790160?text=Hola,%20vengo%20de%20su%20sitio%20web%20y%20me%20gustaría%20agendar%20una%20evaluación%20dental." class="button_primary w-inline-block">Agendar cita para mi hijo</a>
                    </div>
                    <div style="flex: 1; min-width: 300px;">
                        <img src="assets/img/gen_dentist-examining-patients-teeth-close-up_1.jpg" alt="Dentista" style="width: 100%; border-radius: 10px;" />
                    </div>
                </div>
                """
                section.clear()
                section.append(BeautifulSoup(new_html, 'html.parser'))

        # Header menu
        for nav in soup.find_all('nav'):
            for a in nav.find_all('a'):
                if a.text and 'Home' in a.text: a.string = 'Inicio'
                elif a.text and 'About' in a.text: a.string = 'Sobre Nosotros'
                elif a.text and 'Services' in a.text: a.string = 'Servicios'
                elif a.text and 'Blog' in a.text: a.decompose()
            
            for dropdown in soup.find_all('div', class_=re.compile(r'dropdown')):
                if dropdown.text and 'Pages' in dropdown.text: dropdown.decompose()

        # Hero Section
        for h1 in soup.find_all('h1'):
            if h1.text and ('Trusted Dental Care' in h1.text or h1.find(string=re.compile(r'Dental Care'))):
                h1.clear(); h1.append(BeautifulSoup("Sonrisas sanas,<br>atención de primera.", 'html.parser'))
        
        for p in soup.find_all(['p', 'div']):
            if p.string:
                if 'Westside Dentist is a modern dental clinic' in p.string: p.string = "Especialistas Dentales Integrados en Villa Nueva. Agenda tu cita en segundos."
                if 'Ready for a healthier smile?' in p.string: p.string = "¿Listo para una sonrisa más sana? Agenda tu visita hoy."
                if 'Trusted experts caring' in p.string: p.string = "Expertos de confianza cuidando tu sonrisa"
                if 'Personalized Care' in p.string: p.string = "Atención personalizada"
                if 'Hundreds of satisfied' in p.string: p.string = "Cientos de pacientes satisfechos"

        for form in soup.find_all('form'):
            parent = form.find_parent('div')
            if parent:
                for tag in parent.find_all(['h2', 'h3', 'div', 'p']):
                    if tag.string:
                        if 'Book Your' in tag.string: tag.string = "Agenda tu cita"
                        if 'We’ll get back to you' in tag.string: tag.string = "Te responderemos por WhatsApp de inmediato"
            
            for input_tag in form.find_all('input'):
                if input_tag.get('placeholder') and 'Name' in input_tag.get('placeholder'): input_tag['placeholder'] = 'Tu nombre'
                if input_tag.get('placeholder') and 'Phone' in input_tag.get('placeholder'): input_tag['placeholder'] = 'Tu teléfono'
            
            for btn in form.find_all(['button', 'input']):
                if btn.name == 'input' and btn.get('type') == 'submit': btn['value'] = "Solicitar Cita"
                elif btn.string and 'Request Appointment' in btn.string: btn.string = "Solicitar Cita"
        
        for tag in soup.find_all(['div', 'h2', 'h3', 'p']):
            if tag.string:
                if 'Book an Appointment' in tag.string: tag.string = "Agenda tu Cita"
                if 'Direct Contact' in tag.string: tag.string = "Contacto Directo"
                if 'Working Hours' in tag.string: tag.string = "Horarios de Atención"
                if 'Monday - Friday' in tag.string: tag.string = "Lun - Vie: 8:00 - 17:00"
                if 'Saturday - Sunday' in tag.string: tag.string = "Sáb - Dom: 9:30 - 17:30"
                if 'Monday-Friday' in tag.string: tag.string = "Lun - Vie: 8:00 - 17:00"
                if 'Saturday-Sunday' in tag.string: tag.string = "Sáb - Dom: 9:30 - 17:30"
        
        # Services are handled by fix_services.py
        
        for tag in soup.find_all(['h2', 'h3']):
            if tag.string and ('Our Specialists' in tag.string or 'Our Team' in tag.string): tag.string = "Nuestros Especialistas"
        
        for team_card in soup.find_all('div', class_=re.compile(r'team', re.I)):
            name_tag = team_card.find(['h3', 'h4'])
            if name_tag: name_tag.string = "Especialista en Ortodoncia"
            role_tag = team_card.find('div', class_=re.compile(r'role|job', re.I))
            if role_tag: role_tag.string = ""

        for tag in soup.find_all(['h2', 'h3']):
            if tag.string and 'Real Patient' in tag.string: tag.string = "Testimonios Reales"
        
        testis = soup.find_all('div', class_=re.compile(r'testimonial.*item|card', re.I))
        if len(testis) >= 2:
            p1 = testis[0].find('p')
            if p1: p1.string = "Excelente servicio en todos los aspectos. El equipo es muy profesional, atento y amable."
            n1 = testis[0].find(['h4', 'h5', 'div'], class_=re.compile(r'name|author', re.I))
            if n1: n1.string = "Stefano Girón"
            p2 = testis[1].find('p')
            if p2: p2.string = "Muy buen servicio, las secretarias muy amables al explicar el procedimiento."
            n2 = testis[1].find(['h4', 'h5', 'div'], class_=re.compile(r'name|author', re.I))
            if n2: n2.string = "Brenda Mariana"

        for faq in soup.find_all('div', class_=re.compile(r'faq.*item|accordion', re.I)):
            if 'insurance' in faq.text.lower() or 'seguros' in faq.text.lower(): faq.decompose()
        
        for tag in soup.find_all(['h2', 'h3']):
            if tag.string and 'Frequently Asked' in tag.string: tag.string = "Preguntas Frecuentes"
        
        for tag in soup.find_all(['h2', 'h3', 'h1']):
            if tag.string and 'Let’s talk about your smile' in tag.string: tag.string = "Hablemos de tu sonrisa, estamos listos para atenderte"

        html_content = str(soup)
        html_content = re.sub(r'Lumora Dental|Westside Dentist', 'Especialistas Dentales Integrados', html_content)
        html_content = re.sub(r'\+1\s*\(\d{3}\)\s*\d{3}-\d{4}', '5979-0160', html_content)
        html_content = re.sub(r'tel:[\d\+\-\s]+', 'tel:5979-0160', html_content)
        html_content = re.sub(r'\(414\)\s*809\s*-\s*8567', '5979-0160', html_content)
        html_content = re.sub(r'1-800-123-4567', '5979-0160', html_content)
        html_content = re.sub(r'\(\d{3}\)\s*\d{3}-\d{4}', '5979-0160', html_content)

        html_content = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', 'claudiamarissac@gmail.com', html_content)

        html_content = re.sub(r'123 Dental Way.*?USA', 'Centro Médico de Villa Nueva, Zona 4, Colonia Venecia II', html_content)
        html_content = re.sub(r'456 Smile Avenue.*?NY 10001', 'Centro Médico de Villa Nueva, Zona 4, Colonia Venecia II', html_content)
        html_content = re.sub(r'123 Westside Ave, New York, NY 10001', 'Centro Médico de Villa Nueva, Zona 4, Colonia Venecia II', html_content)
        html_content = re.sub(r'123 Westside Ave.*?10001', 'Centro Médico de Villa Nueva, Zona 4, Colonia Venecia II', html_content)

        wa_link = 'https://wa.me/50259790160?text=Hola,%20vengo%20de%20su%20sitio%20web%20y%20me%20gustaría%20agendar%20una%20evaluación%20dental.'
        html_content = re.sub(r'href="[^"]*(cal\.com|book|appointment|contact)[^"]*"', f'href="{wa_link}"', html_content)
        
        with open(filepath, 'w', encoding='utf-8') as f: f.write(html_content)

    css_files = glob.glob('assets/css/*.css')
    for css in css_files:
        with open(css, 'r', encoding='utf-8') as f: css_content = f.read()
        
        css_content = re.sub(r'--primitive-color--primary-900:\s*#[0-9a-fA-F]+;', '--primitive-color--primary-900: #001f3f;', css_content)
        css_content = re.sub(r'--primitive-color--primary-800:\s*#[0-9a-fA-F]+;', '--primitive-color--primary-800: #003366;', css_content)
        css_content = re.sub(r'--primitive-color--primary-700:\s*#[0-9a-fA-F]+;', '--primitive-color--primary-700: #004080;', css_content)
        css_content = re.sub(r'--primitive-color--primary-600:\s*#[0-9a-fA-F]+;', '--primitive-color--primary-600: #0059b3;', css_content)
        css_content = re.sub(r'--primitive-color--primary-500:\s*#[0-9a-fA-F]+;', '--primitive-color--primary-500: #0073e6;', css_content)
        css_content = re.sub(r'--primitive-color--primary-400:\s*#[0-9a-fA-F]+;', '--primitive-color--primary-400: #3399ff;', css_content)
        
        with open(css, 'w', encoding='utf-8') as f: f.write(css_content)

if __name__ == '__main__':
    process_file()
