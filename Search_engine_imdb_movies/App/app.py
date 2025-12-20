import streamlit as st
import pandas as pd

lista_filmes = pd.read_csv('../base_dados/filmes_imdb.csv')

# --- Barra superior da página --- #

st.set_page_config(
    page_title="Pesquisa de Filmes",
    page_icon="../multimedia/page_icon.ico",  # Pode ser emoji, caminho de arquivo ou URL
    layout="wide"
)

# --- Barra lateral --- #

with st.sidebar:
    st.header('Menu')
    butao_lista = st.button('Lista de filmes')
    if butao_lista:
        st.write('Filmes')
        st.write(lista_filmes['Movie Name'])

# --- Página principal --- #
   
st.title('Search Engine de filmes do IMDB')

st.header('')

filme = st.text_input('Nome do Filme:', placeholder= 'Escreva aqui o nome do filme')

pesquisar = st.button('Pesquisar')

if pesquisar:
    st.subheader('Resultado da Pesquisa')