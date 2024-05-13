
import json


class ScrapMaster():
    def __init__(self, soup) -> None:
        script_tag = soup.find('script', string=lambda text: 'window.dataLayer' in str(text))
        json_data = json.loads(script_tag.string.split(' = ')[-1])[0]
        self.ap_data = json_data['page']['adProperties']
        self.ap_page = json_data['page']
        self.soup = soup

    def find_price(self):
        return self.ap_page['detail']['price'] if (self.ap_page['detail']['price']).isdigit() else '0'

    def find_condominio(self):
        condom = "-1"
        father_all = self.soup.find_all('div', class_='ad__sc-1d6de9c-1 idZreM olx-d-flex')
        for father in father_all:
            if 'Condomínio' in str(father):
                condom_div = father.find('span', class_='olx-text olx-text--body-small olx-text--block olx-text--semibold')
                condom = condom_div.text if condom_div is not None else ''
        return condom

    def find_iptu(self):
        iptu = "-1"
        father_all = self.soup.find_all('div', class_='ad__sc-1d6de9c-1 idZreM olx-d-flex')
        for father in father_all:
            if 'IPTU' in str(father):
                iptu_div = father.find('span', class_='olx-text olx-text--body-small olx-text--block olx-text--semibold')
                iptu = iptu_div.text if iptu_div is not None else ''
        return iptu

    def find_anuncio(self):
        anuncio = "-1"
        father_all = self.soup.find_all('span', class_='olx-text olx-text--title-medium olx-text--block ad__sc-1l883pa-2 bdcWAn')
        for father in father_all:
            if ('Detalhes' not in str(father)) and ('Localização' not in str(father)) :
                anuncio = father.text if father is not None else ''
        return anuncio

    def find_descri(self):
        father_all = self.soup.find_all('span', class_='olx-text olx-text--body-medium olx-text--block olx-text--regular ad__sc-2mjlki-1 hNWZgC')
        if len(father_all) > 0:
            return father_all[0].text
        return "-1"

    def find_loc(self):
        loc = "-1"
        father_all = self.soup.find_all('div', class_='ad__sc-1l883pa-1 hZOMmY olx-container olx-container--outlined olx-d-flex olx-ai-flex-start olx-fd-column')
        for father in father_all:
            if 'Localização' in str(father):
                loc_div = father.find('span', class_='olx-text olx-text--body-medium olx-text--block olx-text--semibold')
                loc = loc_div.text if loc_div is not None else ''
        return loc

    def find_endereco(self):
        endereco = ''
        father_all = self.soup.find_all('div', class_='ad__sc-1l883pa-1 hZOMmY olx-container olx-container--outlined olx-d-flex olx-ai-flex-start olx-fd-column')
        for father in father_all:
            if 'Localização' in str(father):
                endereco_div = father.find('span', class_='olx-text olx-text--body-small olx-text--block olx-text--semibold olx-color-neutral-110')
                endereco = endereco_div.text if endereco_div is not None else ''
        return endereco

    def find_vendedor(self):
        script_tag = self.soup.find('script', string=lambda text: 'window.dataLayer' in str(text))
        json_data = json.loads(script_tag.string.split(' = ')[-1])[0]
        return json_data['page']['adDetail']['sellerName']

    def is_profissional(self):
        script_tag = self.soup.find('script', string=lambda text: 'window.dataLayer' in str(text))
        json_data = json.loads(script_tag.string.split(' = ')[-1])[0]
        if json_data['page']['adDetail']['professionalAd'] == True:
            return True
        return False

    def n_fotos(self):
        script_tag = self.soup.find('script', string=lambda text: 'window.dataLayer' in str(text))
        json_data = json.loads(script_tag.string.split(' = ')[-1])[0]
        return json_data['pictures']

    def find_m_quadrado(self):
        for i in self.ap_data:
            if i['name'] == 'size':
                return i['value']    
            
    def is_apertamento(self):
        for i in self.ap_data:
            if i['label'] == 'Categoria':
                if i['value'] == 'Apartamentos':
                    return True   
                return False
            
    def n_quartos(self):
        for i in self.ap_data:
            if i['name'] == 'rooms' :
                return i['value'] 

    def n_banheiros(self):
        for i in self.ap_data:
            if i['name'] == 'bathrooms' :
                return i['value'] 
        
    def n_garagens(self):
        for i in self.ap_data:
            if i['name'] == 'garage_spaces':
                return i['value'] 
            
    def is_academia(self):
        for i in self.ap_data: 
            if i['name'] == 're_features':# procura nas caracteristias do imovel
                values = i['value']
                if 'Academia' in values:
                    return True
            if i['name'] == 're_complex_features':# procura nas caracteristias do imovel
                values = i['value']
                if 'Academia' in values:
                    return True
        return False
            

    def is_churrasqueira(self):
        for i in self.ap_data:
            if i['name'] == 're_features':
                values = i['value']
                if 'Churrasqueira' in values:
                    return True
            if i['name'] == 're_complex_features':# procura nas caracteristias do imovel
                values = i['value']
                if 'Churrasqueira' in values:
                    return True
        return False
            
    def is_piscina(self):
        for i in self.ap_data:
            if i['name'] == 're_features':
                values = i['value']
                if 'Piscina' in values:
                    return True
            if i['name'] == 're_complex_features':# procura nas caracteristias do imovel
                values = i['value']
                if 'Piscina' in values:
                    return True
        return False
            
    def is_varanda(self):
        for i in self.ap_data:
            if i['name'] == 're_features':
                values = i['value']
                if 'Varanda' in values:
                    return True
                break
        return False
            
    def is_elevador(self):
        for i in self.ap_data:
            if i['name'] == 're_complex_features':
                values = i['value']
                if 'Elevador' in values:
                    return True
                break
        return False

    def is_portaria(self):
        for i in self.ap_data:
            if i['name'] == 're_complex_features':
                values = i['value']
                if 'Portaria' in values:
                    return True
                break
        return False
            
    def is_salao_festa(self):
        for i in self.ap_data:
            if i['name'] == 're_complex_features':
                values = i['value']
                if 'Salão de festas' in values:
                    return True
                break
        return False

    def is_mobiliado(self):
        for i in self.ap_data:
            if i['name'] == 're_features':
                values = i['value']
                if 'Mobiliado' in values:
                    return True
                break
        return False

    def is_ar_condicionado(self):
        for i in self.ap_data:
            if i['name'] == 're_features':
                values = i['value']
                if 'Ar condicionado' in values:
                    return True
                break
        return False
