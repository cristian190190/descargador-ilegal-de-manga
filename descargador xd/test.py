import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlretrieve

# Función para obtener el HTML de una página


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


# Función para extraer los links de los capítulos
def get_chapter_links(manga_url):
    html = get_html(manga_url)
    soup = BeautifulSoup(html, 'html.parser')
    chapter_links = []

    # Encuentra todos los divs con la clase "chapter__actions" y extrae los hrefs
    for chapter_div in soup.find_all('div', class_='chapter__actions'):
        a_tag = chapter_div.find('a', href=True)
        if a_tag:
            chapter_links.append(urljoin(manga_url, a_tag['href']))

    return chapter_links

# Función para obtener los links de las imágenes de cada capítulo


def get_image_links(chapter_url):
    html = get_html(chapter_url)
    soup = BeautifulSoup(html, 'html.parser')
    image_links = []

    # Encuentra todos los divs con la clase "reader__item" y extrae los data-srcs
    for img_div in soup.find_all('div', class_='reader__item'):
        img_tag = img_div.find('img', {'data-src': True})
        if img_tag:
            image_links.append(urljoin(chapter_url, img_tag['data-src']))

    return image_links
            


# Función para descargar todas las imágenes de un capítulo
def download_images(image_links, chapter_number):
    # Crear una carpeta para el capítulo
    folder_name = f'Capitulo_{chapter_number}'
    os.makedirs(folder_name, exist_ok=True)

    # Descargar cada imagen en la carpeta correspondiente
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    for idx, img_url in enumerate(image_links):
        image_path = os.path.join(folder_name, f'image_{idx + 1}.jpg')

        # Descargar la imagen usando requests con el encabezado
        response = requests.get(img_url, headers=headers)
        response.raise_for_status()  # Esto lanzará un error si la descarga falla

        # Guardar la imagen en el directorio correspondiente
        with open(image_path, 'wb') as f:
            f.write(response.content)

        print(f'Descargado: {image_path}')


# Función principal
def main(manga_url):
    chapter_links = get_chapter_links(manga_url)
    print(f'Encontrados {len(chapter_links)} capítulos.')

    for chapter_number, chapter_url in enumerate(chapter_links, start=1):
        print(f'Procesando Capítulo {chapter_number}: {chapter_url}')
        image_links = get_image_links(chapter_url)
        print(f' - Encontradas {len(image_links)} imágenes.')
        download_images(image_links, chapter_number)

if __name__ == "__main__":
    manga_url = input("Introduce la URL del manga: ")
    main(manga_url)
