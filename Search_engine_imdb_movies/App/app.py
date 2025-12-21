import streamlit as st
import pandas as pd
import busca

lista_filmes = pd.read_csv('../base_dados/filmes_imdb.csv')

# --- Barra superior da página --- #

st.set_page_config(
    page_title="Pesquisa de Filmes",
    page_icon="../multimedia/page_icon.ico",
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
  
st.title(':streamlit: :blue[Filmes top 1000 do IMDB]', text_alignment = 'center', )

st.write('Este é um motor de busca onde podes procurar através de uma palavra-chave pelo filme que pretendes saber mais informações.')

col1, col2 = st.columns(2)

with col1:
    
    with st.container():
        
        filme = st.text_input('Nome do Filme:', placeholder= 'Escreva aqui o nome do filme', width = 500)

        pesquisar = st.button('Pesquisar')
 
        if pesquisar:
            
            st.session_state.lista.clear()
            
            if 'lista' not in st.session_state:
                st.session_state.lista = []
            
            st.subheader('Resultado da Pesquisa:')
            
            with st.container(border= False, width= 500):
                
                if len(filme) >= 3:
            
                    resultado = busca.busca(filme)

                    for nome, corr, index in resultado:
                        st.write(f'✅ {nome} (Semelhança: {corr :.1f} %)')
                        st.session_state.lista.append(nome)
                    
                else:
                    st.error('Digite no mínimo 3 caracteres para a pesquisa')
        
with col2:
    nome_filme = st.selectbox('Lista de filmes', st.session_state.lista, placeholder='Filme')
    st.header(nome_filme) # Nome do Filme
    st.subheader() # Ano do Filme
    st.write() # Descrição do filme