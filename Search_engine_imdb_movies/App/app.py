import streamlit as st
import pandas as pd
import busca

lista_filmes = pd.read_csv('../base_dados/filmes_imdb.csv')

# --- Barra superior da página --- #

# Configuração do separador da página

st.set_page_config(
    page_title="Pesquisa de Filmes",            # Nome do separador da página
    page_icon="../multimedia/page_icon.ico",    # Icon do separador da página
    layout="wide"                               
)

# --- Barra lateral --- #

with st.sidebar:
    st.header('Menu')
    botao_lista = st.button('Lista de filmes')
    botao_imdb = st.link_button('IMDB', 'https://www.imdb.com')
    botao_limpar = st.button('Limpar')
    
    if botao_limpar:
        st.empty()
        
    if botao_lista:
        st.write('Filmes')
        st.write(lista_filmes['Movie Name'])


# --- Página principal --- #

# Título da página (Centrado, de cor azul com emoji do streamlit no início)

st.title(':streamlit: :blue[Top 1000 filmes do IMDB]', text_alignment = 'center', )

# Breve descrição da página e a sua finalidade

st.write('Este é um motor de busca onde podes procurar através de uma palavra-chave pelo filme que pretendes saber mais informações.')

# Divisão em duas colunas o corpo da página

col1, col2 = st.columns(2)

# Inclusão da 'lista' para guardar os dados que nela entrem.

# Iniciação de um dicionário

if 'lista_pesquisa' not in st.session_state:
    st.session_state.lista_pesquisa = {}

# --- Coluna de pesquisa --- #

# Na coluna 1 irão estar contidos um campo para inserir os termos da pesquisa e os resultados da pesquisa que dai resultarem.

with col1:
        
    filme = st.text_input('Nome do Filme:', placeholder= 'Escreva aqui o nome do filme', width = 500)

    butao_pesquisar = st.button('Pesquisar', type='primary')

    if butao_pesquisar:
        
        st.session_state.lista_pesquisa.clear()
        
        st.subheader('Resultado da Pesquisa:')
        
        #with st.container(border= False, width= 500):
            
        if len(filme) >= 3:
    
            resultado = busca.busca(filme)

            for nome, corr, index in resultado:
                st.write(f'✅ {nome} (Semelhança: {corr :.1f} %)')

                st.session_state.lista_pesquisa[nome] = [corr, index]
        else:
            st.error('Digite no mínimo 3 caracteres para a pesquisa')

# --- Coluna de detalhes do filme --- #
        
with col2:
    
    nome_filme = st.selectbox('Lista de filmes', st.session_state.lista_pesquisa, placeholder='Filme', index= None)
    
    if nome_filme != None:                  # Se o campo nome_filme estiver preenchido.
        st.header(nome_filme)               # Nome do Filme
        
        st.subheader(lista_filmes.iloc[st.session_state.lista_pesquisa[nome_filme][1]]['Year of Release'])                     # Ano do Filme
        
        st.write(f'Duração do filme: *{lista_filmes.iloc[st.session_state.lista_pesquisa[nome_filme][1]]['Watch Time']}* min')

        st.write(f'Descrição: ":blue[{lista_filmes.iloc[st.session_state.lista_pesquisa[nome_filme][1]]['Description']}]"')                     # Descrição do filme