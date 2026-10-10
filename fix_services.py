import glob
from bs4 import BeautifulSoup

def fix_services():
    for filepath in glob.glob('*.html'):
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')

        # Find all service items
        service_wraps = soup.find_all('div', class_='service_item-wrap')
        if not service_wraps:
            continue

        # We want to keep 3 services.
        # Let's define the 3 services:
        services_data = [
            {
                "title": "Odontología Preventiva",
                "desc": "Evaluaciones y limpiezas profundas para tu salud bucal."
            },
            {
                "title": "Ortodoncia",
                "desc": "Pequeños movimientos pueden generar grandes cambios en tu sonrisa."
            },
            {
                "title": "Odontopediatría",
                "desc": "Las mejores sonrisas se construyen con buenos hábitos desde niños."
            }
        ]

        for i, wrap in enumerate(service_wraps):
            if i < 3:
                # Update title
                title_div = wrap.find('div', class_='service-item_info-title')
                if title_div:
                    title_div.string = services_data[i]["title"]
                
                # Update description
                # The description is usually in a <p> next to the title
                p = wrap.find('p')
                if p:
                    p.string = services_data[i]["desc"]
            else:
                # Decompose the 4th and subsequent services
                wrap.decompose()

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))

if __name__ == '__main__':
    fix_services()
