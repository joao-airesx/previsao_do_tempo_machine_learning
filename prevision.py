import numpy as np
import pandas as pd
# para visualização
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
data = pd.read_csv('Clima.csv', index_col=0)
data = pd.melt(data, id_vars='ANO', value_vars=data.columns[1:])

data.rename(columns={'variable': 'VARIAVEL'}, inplace=True)
data.rename(columns={'value': 'VALOR'}, inplace=True)

data['DATA'] = data['VARIAVEL'] + ' ' + data['ANO'].astype(str)

data.loc[:, 'DATA'] = data['DATA'].apply(lambda x: datetime.strptime(x, '%b %Y')).dt.date

# Temperatura ao longo do tempo

data.columns = ['ANO', 'MÊS', 'TEMPERATURA', 'DATA']
data.sort_values(by='DATA', inplace=True)  # para obter a série temporal correta
figura = go.Figure(layout=go.Layout(yaxis=dict(range=[0, data['TEMPERATURA'].max() + 1])))
figura.add_trace(go.Scatter(x=data['DATA'], y=data['TEMPERATURA']), )
figura.update_layout(title='Temperatura ao Longo da Linha do Tempo',
                     xaxis_title='Tempo', yaxis_title='Temperatura em Graus')
figura.update_layout(xaxis=go.layout.XAxis(
    rangeselector=dict(
        buttons=list([dict(label='Visão Total', step='all'),
                      dict(count=1, label='Visualização de Um Ano', step='year', stepmode='todate')
                      ])),
    rangeslider=dict(visible=True), type='date')
)
figura.show()

figura = px.box(data, 'MÊS', 'TEMPERATURA')
figura.update_layout(title='Temperatura mensal mais quente, mais fria e na média')

figura.show()

from sklearn.cluster import KMeans

erros = []
alvo = data['TEMPERATURA'].to_numpy().reshape(-1, 1)
num_clusters = list(range(1, 10))

for k in num_clusters:
    km = KMeans(n_clusters=k)
    km.fit(alvo)
    erros.append(km.inertia_)

figura = go.Figure(data=[
    go.Scatter(x=num_clusters, y=erros, mode='lines'),
    go.Scatter(x=num_clusters, y=erros, mode='markers')
])

figura.update_layout(title='Avaliação do número de clusters:',
                     xaxis_title='Número de Clusters:',
                     yaxis_title='Soma da distância ao quadrado:',
                     showlegend=False)

figura.show()

km = KMeans(3)
km.fit(data['TEMPERATURA'].to_numpy().reshape(-1, 1))
data.loc[:, 'ROTULOS DE TEMPERATURA'] = km.labels_
figura = px.scatter(data, 'DATA', 'TEMPERATURA', color='ROTULOS DE TEMPERATURA')
figura.update_layout(title='Temperatura Cluster',
                     xaxis_title='Data',
                     yaxis_title='Temperatura')

figura.show()

# Cria um histograma da coluna 'TEMPERATURA' do DataFrame 'data'
# nbins=200 define o número de intervalos (barras) no histograma
# histnorm='density' indica que estamos plotando a densidade de probabilidade
figura = px.histogram(x=data['TEMPERATURA'], nbins=200, histnorm='density')
figura.update_layout(title='Gráfico de frequência das leituras de temperatura:',
                     xaxis_title='Temperatura', yaxis_title='Contagem')

figura.show()

data['MEDIA ANUAL'] = data.iloc[:,1:].mean(axis=1)
figura = go.Figure(data[
    go.Scatter(name='Temperatura Anual', x=data['ANO'], y=data['MEDIA ANUAL'], mode='lines'),
    go.Scatter(name='Temperatura Anual', x=data['ANO'], y=data['MEDIA ANUAL'], mode='markers')
                 ])
figura.update_layout(title='Temperatura Média Anual:',
                     xaxis_title='Tempo',
                     yaxis_title='Temperatura em Graus')

figura.show()

print(data.head())
