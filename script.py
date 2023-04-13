from bs4 import BeautifulSoup
import requests
import pandas as pd

df = pd.DataFrame()
df['Nombre'] = None
df['Tipo'] = None
df['Website'] = None
url = 'https://www.gualeguaychu.tur.ar/alojamiento/'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
accomodation_types = soup.find_all('div', class_='elementor-shortcode')

for accomodation_type in accomodation_types:
    gallery_containers = accomodation_type.find_all(
        'div', 'rl-gallery-container')
    if (len(gallery_containers)):
        for gallery_container in gallery_containers:
            galleries = gallery_container.find_all("div", "rl-gallery")
            title = 'La web no especifica el tipo'
            if (gallery_container.find("h4", 'rl-gallery-title') is not None):
                title = gallery_container.find("h4", 'rl-gallery-title').text
            if (len(galleries)):
                for gallery in galleries:
                    items = gallery.find_all("div", "rl-gallery-item")
                    if (len(items)):
                        for item in items:
                            title_item = item.find(
                                "span", 'rl-gallery-item-title')
                            link_item = item.find(
                                "a", class_="rl-gallery-link")
                            if (link_item is not None):
                                row_in_df = {
                                    'Nombre': title_item.text, 'Tipo': title, 'Website': link_item['href'] if link_item['href'] is not None else ''}
                            else:
                                row_in_df = {
                                    'Nombre': title_item.text, 'Tipo': title}
                            df = df.append(row_in_df, ignore_index=True)
    else:
        paragraphs = accomodation_type.find_all("p")
        if (len(paragraphs)):
            for paragraph in paragraphs:
                paragraphs_titles = paragraph.find_all("b")
                if (len(paragraphs_titles)):
                    for title_accomodation in paragraphs_titles:
                        if (len(title_accomodation.text) > 1):
                            row_in_df = {'Nombre': title_accomodation.text,
                                         'Tipo': 'La web no especifica el tipo'}
                            df = df.append(row_in_df, ignore_index=True)


file_name_csv = "alojamientos.csv"
file_name_excel = "alojamientos.xlsx"
df.to_csv(file_name_csv)
print("Accomodations saved in csv")
df.to_excel(file_name_excel)
print("Accomodations saved in excel")
