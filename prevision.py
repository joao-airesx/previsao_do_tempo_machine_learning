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
print(data.head())
