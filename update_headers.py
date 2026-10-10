import os
import re
from bs4 import BeautifulSoup

def process_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Skipping {filename}: {e}")
        return

    soup = BeautifulSoup(content, 'html.parser')
    modified = False

    header = soup.find('div', class_=lambda c: c and 'navbar' in c) or soup.find('header')
    if header:
        btn = header.find(string=lambda text: text and 'Get Appointment' in text)
        if btn:
            btn.replace_with('Agendar Cita')
            a_tag = btn.find_parent('a')
            if a_tag:
                a_tag['href'] = "https://wa.me/50259790160"
                a_tag['target'] = "_blank"
                modified = True

    if modified:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated {filename}")

def main():
    files = ['index.html', 'about.html', 'service.html', 'blog.html']
    for file in files:
        if os.path.exists(file):
            process_file(file)

if __name__ == '__main__':
    main()
