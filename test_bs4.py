
from bs4 import BeautifulSoup
html = '''<div class=\"service-item_tag\">
 <div class=\"service-tag_icon\">
  <svg></svg>
 </div>
 <div>
  Checkups
 </div>
</div>'''
soup = BeautifulSoup(html, 'html.parser')
for pill in soup.find_all('div', class_='service-item_tag'):
    for inner_div in pill.find_all('div'):
        if 'service-tag_icon' in inner_div.get('class', []): continue
        if 'checkups' in inner_div.text.lower():
            inner_div.string = 'Salud Dental'
print(soup.prettify())

