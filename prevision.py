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

data.loc[:, 'DATA'] = data['DATA'].apply(lambda x: datetime.strptime(x , '%b %Y')).dt.date

print(data.head())
