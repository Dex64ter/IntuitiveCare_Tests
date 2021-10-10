import requests
from bs4 import BeautifulSoup
import os

def searchWeb(site):
    for word in site:
        if(word[0:5] == 'href='):
            break
    
    return word[5:].replace('"', "")

def search(u):
    webpage = requests.get(u)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    standards = soup.select('.callout')

    site = str(standards[0]).split(' ')
    return site

url = 'https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss'

site = search(url)

url2 = searchWeb(site)

webpage2 = requests.get(url2)
soup2 = BeautifulSoup(webpage2.content, 'html.parser') 
documents = soup2.select('tbody td a')
documents = searchWeb(str(documents[0]).split(' '))

cwd = os.path.dirname(os.path.realpath(__file__))
file = requests.get(documents, allow_redirects=True).content
with open(f'{cwd}/padrao_tiss_componente_organizacional_202108.pdf', 'wb') as pdf:
    pdf.write(file)

