# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 21:46:00 2021
@author: unily
"""
# I: Importando librerias
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import date
import time, re, os
import plotly.express as px
from plotly.offline import plot
# Arrancando el webdriver:
options = Options()
options.add_argument("--lang=es")
driver = webdriver.Chrome(r'', chrome_options=options)

# II: Descargando y procesando datos
universidad = 'Universidades'
paises = ['Chile', 'Argentina', 'Colombia', 'México', 'Panamá', 'Ecuador', 'Uruguay', 'Perú', 'Nicaragua', 'Guatemala', 'Bolivia', 'Brasil']

for pais in paises:
    url = 'https://www.google.com/maps/search/' + universidad + ' ' + pais
# Cargando el url
    driver.get(url)
# Esperando que la información esté visible y ejecutando crawler:
    time.sleep(5)
    texto = []
    while True:
        try:
            results = [i.text for i in driver.find_elements_by_class_name('lI9IFe')]            
            texto.append(results)
            driver.find_element_by_xpath('/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[4]/div[2]/div/div[1]/div/button[2]/img').click()
            time.sleep(5)
        except:
            break
            pass
    # Manipulacion de listas para crear dataframe
    listas = [i for sublist in texto for i in sublist]            
    data = pd.DataFrame(listas)
    data = data[0].str.split('\n', expand=True)
    data['rating'] = data[1].str.extract('(\d.\d)')
    data['votos'] = data[1].str.extract(r'\((\d+)\)')
    data['pais'] = pais
    #Guardando archivos csv
    data.to_csv(r'{0}_{1}.csv'.format(pais, date.today()), index = False)

#Uniendo y filtrando bases
path = ''
os.chdir(path)
for path, subdirs, files in os.walk(path):
    for name in files:
        print(files)
combined_csv = pd.concat([pd.read_csv(f) for f in files],ignore_index = True)
combined_csv.drop(combined_csv.filter(regex="Unname"),axis=1, inplace=True)
combined_csv2 = combined_csv.loc[combined_csv['votos'] >= 500].sort_values('votos')[-20:]
ranking = combined_csv2[['0','votos','rating', 'pais']]
ranking['rating'] = ranking['rating'].str.replace(',','.')
ranking['rating'] = pd.to_numeric(ranking['rating'], errors='coerce')

#III: Gaficando
fig = px.scatter(x = ranking.votos, y = ranking.rating,
                 template = "simple_white", height = 800, text = ranking['0'],
                 size = ranking.votos, size_max=30, color = ranking.pais,
                 title={'text': 'LAC-12, universidades mejor calificadas en google maps (top 15)',
                 'xanchor': 'center',
                 'y': 0.9, 'x': 0.5})
fig.update_layout(showlegend=False, uniformtext_minsize=8, uniformtext_mode='show')
fig.update_traces(textposition="bottom center")
fig.update_layout(
xaxis_title="Número de votos",
xaxis_range = [500, 1200],
yaxis_title="Calificación [1:5]",
yaxis_range = [3.9, 5],
yaxis={'showticklabels': True},
plot_bgcolor='rgba(0,0,0,0)')
plot(fig)
