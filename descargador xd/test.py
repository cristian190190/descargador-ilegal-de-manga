import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def get_chapter_links(manga_url):
    html = get_html(manga_url)
    soup = BeautifulSoup(html, 'html.parser')
    chapter_links = []

    for chapter_div in soup.find_all('div', class_='chapter__actions'):
        a_tag = chapter_div.find('a', href=True)
        if a_tag:
            chapter_links.append(urljoin(manga_url, a_tag['href']))

    return chapter_links


def get_image_links(chapter_url):
    html = get_html(chapter_url)
    soup = BeautifulSoup(html, 'html.parser')
    image_links = []

    for img_div in soup.find_all('div', class_='reader__item'):
        img_tag = img_div.find('img', {'data-src': True})
        if img_tag:
            image_links.append(urljoin(chapter_url, img_tag['data-src']))

    return image_links


def download_images(image_links, folder_name):
    os.makedirs(folder_name, exist_ok=True)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    for idx, img_url in enumerate(image_links):
        image_path = os.path.join(folder_name, f'image_{idx + 1}.jpg')

        response = requests.get(img_url, headers=headers)
        response.raise_for_status()

        with open(image_path, 'wb') as f:
            f.write(response.content)

        print(f'Descargado: {image_path}')


def main(manga_url):
    chapter_links = get_chapter_links(manga_url)
    total_chapters = len(chapter_links)
    print(f'Encontrados {total_chapters} capítulos.')

    # Enumeramos directamente desde el mayor al menor
    for chapter_number, chapter_url in enumerate(chapter_links, start=1):
        actual_chapter_number = total_chapters - chapter_number + 1
        print(f'Procesando Capítulo {actual_chapter_number}: {chapter_url}')
        image_links = get_image_links(chapter_url)
        print(f' - Encontradas {len(image_links)} imágenes.')
        folder_name = f"Capitulo_{actual_chapter_number}"
        download_images(image_links, folder_name)

 
if __name__ == "__main__":
    try:
        manga_url = input("Introduce la URL del manga: ")
        main(manga_url)
    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario. Saliendo del programa...")
