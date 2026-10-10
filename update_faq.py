import os
import re
from bs4 import BeautifulSoup

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. ENCABEZADOS PRINCIPALES
    faq_section = soup.find('section', class_=re.compile('section_faq', re.I))
    if faq_section:
        # Título H2
        for h2 in faq_section.find_all('h2'):
            if 'Questions' in h2.text:
                h2.clear()
                span = soup.new_tag('span', attrs={'class': 'text-highlighted'})
                span.string = "Preguntas"
                h2.append(span)
                h2.append(" Frecuentes")

        # Párrafo descriptivo
        p = faq_section.find('p', class_='body-text-18px')
        if p and 'Answers to Your Most Common Questions' in p.text:
            p.string = "Respuestas a las dudas más comunes sobre nuestro cuidado dental y servicios en la clínica."

        # 2. CAJA DE CONTACTO
        title_q = faq_section.find(string=re.compile('Still have a question', re.I))
        if title_q:
            title_q.replace_with("¿Aún tienes dudas?")
            
        p_team = faq_section.find('p')
        if p_team:
            for pp in faq_section.find_all('p'):
                if 'Our team is ready to assist you' in pp.text:
                    pp.string = "Nuestro equipo está listo para atenderte y agendar tu cita."

        btn_call = faq_section.find(string=re.compile('Make A Call', re.I))
        if btn_call:
            a_tag = btn_call.find_parent('a')
            btn_call.replace_with("Escríbenos")
            if a_tag:
                a_tag['href'] = "https://wa.me/50259790160"
                a_tag['target'] = "_blank"

        # 3. PREGUNTAS DEL ACORDEÓN
        faq_data = {
            "How often should I visit the dentist?": {
                "title": "¿Con qué frecuencia debo visitar al dentista?",
                "ans": "Recomendamos un chequeo dental de rutina y limpieza general cada seis meses para mantener tu boca sana y prevenir cualquier problema a tiempo."
            },
            "Do you offer emergency dental services?": {
                "title": "¿Atienden emergencias dentales?",
                "ans": "Sí, sabemos que el dolor de muelas no avisa. Si tienes una emergencia o dolor fuerte, contáctanos de inmediato a nuestro WhatsApp para buscarte un espacio lo antes posible."
            },
            "Are your treatments painful?": {
                "title": "¿Los tratamientos son dolorosos?",
                "ans": "¡Para nada! Utilizamos técnicas modernas, equipo actualizado y anestesia local para asegurarnos de que tu visita sea totalmente cómoda, segura y sin dolor."
            },
            "What dental services do you provide?": {
                "title": "¿Qué servicios dentales ofrecen?",
                "ans": "Ofrecemos un cuidado integral: ortodoncia (brackets), odontopediatría (atención para niños), limpiezas profundas, extracciones, blanqueamientos y odontología preventiva para toda la familia."
            }
        }

        items = faq_section.find_all('a', class_=re.compile('faq_item', re.I))
        for item in items:
            title_div = item.find('div', class_='faq-header_title')
            if not title_div:
                continue
                
            orig_title = title_div.text.strip()
            
            # 5th question: Do you accept insurance?
            if 'insurance' in orig_title.lower() or 'aseguranzas' in orig_title.lower() or 'seguros' in orig_title.lower():
                item.decompose()
                continue
                
            # Replace mapped questions
            for eng, spa in faq_data.items():
                if eng.lower() in orig_title.lower() or spa['title'].lower() in orig_title.lower():
                    title_div.string = spa['title']
                    ans_div = item.find('div', class_='faq-description_inner')
                    if ans_div:
                        ans_p = ans_div.find('p')
                        if ans_p:
                            ans_p.string = spa['ans']
                    break

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main()
