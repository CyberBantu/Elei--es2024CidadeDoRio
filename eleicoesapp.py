# Importando base de vereadores eleitos
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
# Deixando wide a app
st.set_page_config(layout="wide")

# Importando base de vereadores eleitos shp
df = gpd.read_file('RJ_vereador_eleitos_2024.shp')

st.title('Análise de Votos por Zona Eleitoral em 2024')
st.subheader('Vereadores Eleitos na Cidade do Rio em 2024')

# Criando filtro do streamlit de candidatos eleitos ela coluna NM_URNA_CA
candidato = st.selectbox('Escolha um candidato a Vereador Eleito', df['NM_URNA_CA'].unique())

# Filtrando os dados pelo candidato selecionado
df_filtrado = df[df['NM_URNA_CA'] == candidato]

#Criando uma coluna de % de votos em relação ao totoal de votos arreradados 2 casas e * 100
df_filtrado['perc'] = (df_filtrado['QT_VOTOS_N'] / df_filtrado['QT_VOTOS_N'].sum() * 100).round(2)


# Exibindo informações sobre o candidato
st.subheader('Informações do Candidato')
st.write(f"O candidato escolhido foi: {candidato}")
st.write(f"O candidato escolhido é do partido: {df_filtrado['SG_PARTIDO'].values[0]}")
st.write(f"O candidato escolhido foi: {df_filtrado['DS_SIT_TOT'].values[0]}")

st.write('**O Mapa abaixo mostra o % dos votos distribuidos pelas Zonas Eleitorais**') 
# Criando o mapa interativo
if len(df_filtrado) > 0:
    fig = px.choropleth_mapbox(df_filtrado,
                               geojson=df_filtrado.geometry.__geo_interface__,
                               locations=df_filtrado.index,
                               color='perc',
                               color_continuous_scale="RdYlGn",
                               mapbox_style="carto-positron",
                               zoom=9, center={"lat": -22.9068, "lon": -43.1729},
                               opacity=0.5,
                               labels={'perc': 'Percentual', 'QT_VOTOS_N': 'Quantidade de Votos'},
                               hover_data={'Bairro': True, 'QT_VOTOS_N': True, 'perc': True}
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig)
else:
    st.write("Nenhum dado disponível para o candidato selecionado.")
    
# Função para carregar CSV
@st.cache_data
def carregar_csv(caminho):
    return pd.read_csv(caminho, sep=',', encoding='latin1')

# Carregando os dados
vereadores_cor = carregar_csv('rj_votos_vereadores_raca_2024.csv')
vereadores_genero = carregar_csv('rj_votos_vereadores_genero_2024.csv')

# Criando duas colunas para exibir os gráficos lado a lado
col1, col2 = st.columns(2)

# Gráfico de Votos por Cor
with col1:
    fig_cor = px.bar(
        vereadores_cor, 
        x='Raca', 
        y='%_votos_raca', 
        title='Percentual de Votos por Cor - Vereadores 2024', 
        labels={'Raca': 'Cor do Candidato', '%_votos_raca': 'Percentual de Votos'}
    )
    st.plotly_chart(fig_cor, use_container_width=True)

# Gráfico de Votos por Gênero
with col2:
    fig_genero = px.bar(
        vereadores_genero, 
        x='Genero', 
        y='%_votos_genero', 
        title='Percentual de Votos por Gênero - Vereadores 2024', 
        labels={'Genero': 'Gênero', '%_votos_genero': 'Percentual de Votos'}
    )
    st.plotly_chart(fig_genero, use_container_width=True)









   
# --------------------------------
   
    
# Fazendo as mesmas coisas com uma base de prefeitos
df_prefeito = gpd.read_file('RJ_prefeito_2024.shp')

st.title('Análise de Votos por Zona Eleitoral em 2024')

st.subheader('Votos de Candidatos a Prefeitos do Rio de Janeiro em 2024 por Zona Eleitoral')

# Criando filtro do streamlit de candidatos eleitos ela coluna NM_URNA_CA
candidato_pref = st.selectbox('Escolha um candidato a Prefeito Eleito', df_prefeito['NM_URNA_CA'].unique())

# Filtrando os dados pelo candidato selecionado
df_filtrado_pref = df_prefeito[df_prefeito['NM_URNA_CA'] == candidato_pref]

#Criando uma coluna de % de votos em relação ao totoal de votos arreradados 2 casas e * 100
df_filtrado_pref['perc'] = (df_filtrado_pref['QT_VOTOS_N'] / df_filtrado_pref['QT_VOTOS_N'].sum() * 100).round(2)

# Fazendo o percentual de votos dos candidatos por zona


# Criando o mapa interativo
if len(df_filtrado_pref) > 0:
    fig = px.choropleth_mapbox(df_filtrado_pref,
                               geojson=df_filtrado_pref.geometry.__geo_interface__,
                               locations=df_filtrado_pref.index,
                               color='perc',
                               color_continuous_scale="RdYlGn",
                               mapbox_style="carto-positron",
                               zoom=9, center={"lat": -22.9068, "lon": -43.1729},
                               opacity=0.5,
                               labels={'perc': 'Percentual', 'QT_VOTOS_N': 'Quantidade de Votos'},
                               hover_data={'Bairro': True, 'QT_VOTOS_N': True, 'perc': True}
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig)
