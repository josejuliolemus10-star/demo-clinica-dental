import glob, re
for js_file in glob.glob('assets/js/*.js'):
    try:
        with open(js_file, 'r', encoding='utf-8') as f: content = f.read()
    except UnicodeDecodeError:
        continue
    content = re.sub(r'Lumora Dental|Westside Dentist', 'Especialistas Dentales Integrados', content)
    content = re.sub(r'\+1\s*\(\d{3}\)\s*\d{3}-\d{4}', '5979-0160', content)
    content = re.sub(r'tel:[\d\+\-\s]+', 'tel:5979-0160', content)
    content = re.sub(r'\(414\)\s*809\s*-\s*8567', '5979-0160', content)
    content = re.sub(r'1-800-123-4567', '5979-0160', content)
    content = re.sub(r'\(\d{3}\)\s*\d{3}-\d{4}', '5979-0160', content)
    content = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', 'claudiamarissac@gmail.com', content)
    content = re.sub(r'123 Dental Way.*?USA', 'Centro Médico de Villa Nueva, Zona 4, Colonia Venecia II', content)
    content = re.sub(r'456 Smile Avenue.*?NY 10001', 'Centro Médico de Villa Nueva, Zona 4, Colonia Venecia II', content)
    wa_link = 'https://wa.me/50259790160?text=Hola,%20vengo%20de%20su%20sitio%20web%20y%20me%20gustaría%20agendar%20una%20evaluación%20dental.'
    content = re.sub(r'href="[^"]*(cal\.com|book|appointment|contact)[^"]*"', f'href="{wa_link}"', content)
    with open(js_file, 'w', encoding='utf-8') as f: f.write(content)
