import os
from bs4 import BeautifulSoup

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # 1. TEXTOS Y BOTONES PRINCIPALES:
    # Párrafo: "We combine modern technology with heartfelt service to ensure every generation."
    p = soup.find(string=lambda t: t and 'We combine modern technology' in t)
    if p:
        p.replace_with("Especialistas Dentales Integrados en Villa Nueva.")

    # Botón "Get Appointment"
    btn1 = soup.find(string=lambda t: t and 'Get Appointment' in t)
    if btn1:
        btn1.replace_with("Agendar Cita")

    # Botón "Book Appointment"
    btn2 = soup.find(string=lambda t: t and 'Book Appointment' in t)
    if btn2:
        btn2.replace_with("Agendar Cita")

    # 2. INTERFAZ DEL FORMULARIO (HTML):
    # Título "Book a visit"
    title = soup.find(string=lambda t: t and 'Book a visit' in t)
    if title:
        title.replace_with("Haz una consulta")

    # Subtítulo "Get a callback within 10 minutes"
    sub = soup.find(string=lambda t: t and 'Get a callback within 10 minutes' in t)
    if sub:
        sub.replace_with("Te responderemos directo al WhatsApp")

    # The form itself
    form = soup.find('form', class_='lead-form')
    if form:
        # Remove original onsubmit
        if 'onsubmit' in form.attrs:
            del form.attrs['onsubmit']
        form['id'] = 'heroForm'

        inputs = form.find_all('input')
        if len(inputs) >= 1:
            inputs[0]['placeholder'] = "Tu nombre"
            inputs[0]['id'] = "userName"
        if len(inputs) >= 2:
            inputs[1]['placeholder'] = "Tu pregunta/consulta"
            inputs[1]['id'] = "userQuestion"
            inputs[1]['type'] = "text"

        btn = form.find('button', type='submit')
        if btn:
            btn.string = "Enviar por WhatsApp"
            btn['id'] = "btnWhatsapp"

        note = form.find('div', class_='lead-form_note')
        if note:
            note.string = "Atención rápida y personalizada."

    # 3. LÓGICA DE WHATSAPP (JAVASCRIPT)
    script_content = """
document.addEventListener("DOMContentLoaded", function() {
    const heroForm = document.getElementById('heroForm');
    if(heroForm) {
        heroForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const nombre = document.getElementById('userName').value;
            const pregunta = document.getElementById('userQuestion').value;
            const url = `https://wa.me/50259790160?text=Hola,%20mi%20nombre%20es%20${encodeURIComponent(nombre)}%20y%20tengo%20esta%20duda:%20${encodeURIComponent(pregunta)}`;
            window.open(url, '_blank');
        });
    }
});
"""
    # Append the script before closing body
    new_script = soup.new_tag("script")
    new_script.string = script_content
    
    body = soup.find('body')
    if body:
        body.append(new_script)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == "__main__":
    main()
