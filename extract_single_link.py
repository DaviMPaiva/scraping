import json
import re
import requests
from bs4 import BeautifulSoup

def find_price(soup):
    price = soup.find_all('span', class_='olx-text olx-text--title-large olx-text--block')
    return price[0].text

def find_condominio(soup):
    condom = "-1"
    father_all = soup.find_all('div', class_='ad__sc-1d6de9c-1 idZreM olx-d-flex')
    for father in father_all:
        if 'Condomínio' in str(father):
            condom_div = father.find('span', class_='olx-text olx-text--body-small olx-text--block olx-text--semibold')
            condom = condom_div.text
    return condom

def find_iptu(soup):
    iptu = "-1"
    father_all = soup.find_all('div', class_='ad__sc-1d6de9c-1 idZreM olx-d-flex')
    for father in father_all:
        if 'IPTU' in str(father):
            iptu_div = father.find('span', class_='olx-text olx-text--body-small olx-text--block olx-text--semibold')
            iptu = iptu_div.text
    return iptu

def find_anuncio(soup):
    anuncio = "-1"
    father_all = soup.find_all('span', class_='olx-text olx-text--title-medium olx-text--block ad__sc-1l883pa-2 bdcWAn')
    for father in father_all:
        if ('Detalhes' not in str(father)) and ('Localização' not in str(father)) :
            anuncio = father.text
    return anuncio

def find_descri(soup):
    father_all = soup.find_all('span', class_='olx-text olx-text--body-medium olx-text--block olx-text--regular ad__sc-2mjlki-1 hNWZgC')
    if len(father_all) > 0:
        return father_all[0].text
    return "-1"

def find_loc(soup):
    loc = "-1"
    father_all = soup.find_all('div', class_='ad__sc-1l883pa-1 hZOMmY olx-container olx-container--outlined olx-d-flex olx-ai-flex-start olx-fd-column')
    for father in father_all:
        if 'Localização' in str(father):
            loc_div = father.find('span', class_='olx-text olx-text--body-medium olx-text--block olx-text--semibold')
            loc = loc_div.text
    return loc

def find_endereco(soup):
    endereco = "-1"
    father_all = soup.find_all('div', class_='ad__sc-1l883pa-1 hZOMmY olx-container olx-container--outlined olx-d-flex olx-ai-flex-start olx-fd-column')
    for father in father_all:
        if 'Localização' in str(father):
            endereco_div = father.find('span', class_='olx-text olx-text--body-small olx-text--block olx-text--semibold olx-color-neutral-110')
            endereco = endereco_div.text
    return endereco

def find_vendedor(soup):
    script_tag = soup.find('script', string=lambda text: 'window.dataLayer' in str(text))
    json_data = json.loads(script_tag.string.split('=')[-1])[0]
    return json_data['page']['adDetail']['sellerName']

def is_profissional(soup):
    script_tag = soup.find('script', string=lambda text: 'window.dataLayer' in str(text))
    json_data = json.loads(script_tag.string.split('=')[-1])[0]
    if json_data['page']['adDetail']['professionalAd'] == True:
        return True
    return False

def n_fotos(soup):
    script_tag = soup.find('script', string=lambda text: 'window.dataLayer' in str(text))
    json_data = json.loads(script_tag.string.split('=')[-1])[0]
    return json_data['pictures']

def find_json(soup):
    script_tag = soup.find('script', string=lambda text: 'window.dataLayer' in str(text))
    json_data = json.loads(script_tag.string.split('=')[-1])[0]
    ap_data = json_data['page']['adProperties']
    return ap_data

def find_m_quadrado(ap_data):
    for i in ap_data:
        if i['name'] == 'size':
            return i['value']    
        
def is_apertamento(ap_data):
    for i in ap_data:
        if i['label'] == 'Categoria':
            if i['value'] == 'Apartamentos':
                return True   
            return False
        
def n_quartos(ap_data):
    for i in ap_data:
        if i['name'] == 'rooms' :
            return i['value'] 

def n_banheiros(ap_data):
    for i in ap_data:
        if i['name'] == 'bathrooms' :
            return i['value'] 
    
def n_garagens(ap_data):
    for i in ap_data:
        if i['name'] == 'garage_spaces':
            return i['value'] 
        
def is_academia(ap_data):
    for i in ap_data: 
        if i['name'] == 're_features':# procura nas caracteristias do imovel
            values = i['value']
            if 'Academia' in values:
                return True
        if i['name'] == 're_complex_features':# procura nas caracteristias do imovel
            values = i['value']
            if 'Academia' in values:
                return True
    return False
           

def is_churrasqueira(ap_data):
    for i in ap_data:
        if i['name'] == 're_features':
            values = i['value']
            if 'Churrasqueira' in values:
                return True
        if i['name'] == 're_complex_features':# procura nas caracteristias do imovel
            values = i['value']
            if 'Churrasqueira' in values:
                return True
    return False
        
def is_piscina(ap_data):
    for i in ap_data:
        if i['name'] == 're_features':
            values = i['value']
            if 'Piscina' in values:
                return True
        if i['name'] == 're_complex_features':# procura nas caracteristias do imovel
            values = i['value']
            if 'Piscina' in values:
                return True
    return False
        
def is_varanda(ap_data):
    for i in ap_data:
        if i['name'] == 're_features':
            values = i['value']
            if 'Varanda' in values:
                return True
            break
    return False
        
def is_elevador(ap_data):
    for i in ap_data:
        if i['name'] == 're_complex_features':
            values = i['value']
            if 'Elevador' in values:
                return True
            break
    return False

def is_portaria(ap_data):
    for i in ap_data:
        if i['name'] == 're_complex_features':
            values = i['value']
            if 'Portaria' in values:
                return True
            return False
        
def is_salao_festa(ap_data):
    for i in ap_data:
        if i['name'] == 're_complex_features':
            values = i['value']
            if 'Salão de festas' in values:
                return True
            break
    return False

def is_mobiliado(ap_data):
    for i in ap_data:
        if i['name'] == 're_features':
            values = i['value']
            if 'Mobiliado' in values:
                return True
            break
    return False

def is_ar_condicionado(ap_data):
    for i in ap_data:
        if i['name'] == 're_features':
            values = i['value']
            if 'Ar condicionado' in values:
                return True
            break
    return False


def scrape_website(url, headers=None):
    # Send a GET request to the URL with custom headers
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

    #find_condominio(soup)
    #find_condominio(soup)  
    ap_data = find_json(soup)  
    #is_apertamento(ap_data)
    #print(find_m_quadrado(ap_data))

    with open('webpage.html', 'w', encoding='utf-8') as file:
        file.write(soup.prettify())

# URL of the website you want to scrape
url = "https://pe.olx.com.br/grande-recife/imoveis/proximo-ao-metro-1296501523?lis=listing_1001"

# Custom headers (if needed)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5'
}

# Call the function with the URL and headers
scrape_website(url, headers=headers)

